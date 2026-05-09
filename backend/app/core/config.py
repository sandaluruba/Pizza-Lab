from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Pizza Lab API"
    app_env: str = "development"
    backend_port: int = 8000
    frontend_origin: str = "http://localhost:5173"
    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db: str = "pizza_lab"
    wso2_issuer: str = "https://api.asgardeo.io/t/orgfvzwp/oauth2/token"
    wso2_jwks_url: str = "https://api.asgardeo.io/t/orgfvzwp/oauth2/jwks"
    wso2_audience: str = "MEL8Yk6BwtOgFk_Vf42aBDfBVc8a"
    # Some Asgardeo JWTs use accounts.asgardeo.io issuer; try alt if primary issuer validation fails.
    wso2_issuer_alt: str | None = None
    wso2_verify_tls: bool = True
    # Opaque access tokens: validate via OAuth2 introspection (secret stays on server only).
    asgardeo_introspect_client_id: str | None = None
    asgardeo_introspect_client_secret: str | None = None

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


@lru_cache
def get_settings() -> Settings:
    return Settings()
