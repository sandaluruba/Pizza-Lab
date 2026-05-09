import json
from functools import lru_cache
from typing import Any

import httpx
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import algorithms, get_unverified_header

from app.core.config import Settings, get_settings
from app.schemas.auth import AuthUser

bearer_scheme = HTTPBearer(auto_error=True)


def _looks_like_jwt(token: str) -> bool:
    parts = token.split(".")
    return len(parts) == 3 and all(parts)


@lru_cache
def _jwks() -> dict[str, Any]:
    settings = get_settings()
    response = httpx.get(settings.wso2_jwks_url, verify=settings.wso2_verify_tls, timeout=5.0)
    response.raise_for_status()
    return response.json()


def _introspection_url(settings: Settings) -> str:
    return settings.wso2_jwks_url.replace("/jwks", "/introspect")


def _decode_opaque_via_introspection(token: str) -> dict[str, Any]:
    """Asgardeo often issues opaque reference tokens; JWKS validation only applies to JWT access tokens."""
    settings = get_settings()
    secret = settings.asgardeo_introspect_client_secret
    if not secret:
        raise ValueError(
            "Opaque access token: set ASGARDEO_INTROSPECT_CLIENT_SECRET in backend .env "
            "(or configure Asgardeo to issue JWT access tokens for this app)."
        )
    client_id = settings.asgardeo_introspect_client_id or settings.wso2_audience
    url = _introspection_url(settings)
    response = httpx.post(
        url,
        data={"token": token, "token_type_hint": "access_token"},
        auth=(client_id, secret),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        verify=settings.wso2_verify_tls,
        timeout=10.0,
    )
    response.raise_for_status()
    data = response.json()
    if not data.get("active"):
        raise ValueError("Token is not active.")
    return data


def _decode_jwt(token: str) -> dict[str, Any]:
    settings = get_settings()
    header = get_unverified_header(token)
    kid = header.get("kid")
    keys = _jwks().get("keys", [])
    jwk = next((entry for entry in keys if entry.get("kid") == kid), None)
    if jwk is None:
        raise ValueError("Unable to find signing key.")

    public_key = algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))
    try:
        return jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience=settings.wso2_audience,
            issuer=settings.wso2_issuer,
        )
    except jwt.InvalidIssuerError:
        alt = settings.wso2_issuer_alt
        if not alt:
            raise
        return jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience=settings.wso2_audience,
            issuer=alt,
        )


def _decode_token(token: str) -> dict[str, Any]:
    if not _looks_like_jwt(token):
        return _decode_opaque_via_introspection(token)
    return _decode_jwt(token)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> AuthUser:
    settings = get_settings()
    try:
        payload = _decode_token(credentials.credentials)
    except Exception as exc:  # noqa: BLE001
        detail = "Invalid access token."
        if settings.app_env == "development":
            detail = f"Invalid access token: {exc!s}"
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
        ) from exc

    # JWTs use `sub`; Asgardeo introspection often returns `username` without `sub`.
    user_id = (
        payload.get("sub")
        or payload.get("username")
        or payload.get("preferred_username")
    )
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token subject missing (no sub/username).",
        )

    return AuthUser(
        user_id=str(user_id),
        username=payload.get("preferred_username") or payload.get("username"),
        email=payload.get("email"),
    )
