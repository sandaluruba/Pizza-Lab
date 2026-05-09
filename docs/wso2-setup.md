# Identity setup (Asgardeo — org `orgfvzwp`)

This project uses **[Asgardeo](https://asgardeo.io/)** (WSO2 cloud IdP) with OIDC. Self-hosted WSO2 Identity Server is optional.

Organization path segment: **`orgfvzwp`** (set as `VITE_ASGARDEO_ORG` in `frontend/.env`).

**OIDC discovery note:** Asgardeo may respond with **302** or **404** to  
`https://api.asgardeo.io/t/<org>/.well-known/openid-configuration`  
(so the browser never receives OIDC JSON). This app **does not rely on that URL**: it passes explicit OIDC metadata in code (`issuer`, `authorize`, `token`, `jwks`, etc.) built from your org name—same pattern as Asgardeo’s JS SDK `baseUrl`.

**Token / JWKS** (backend env vars) use `/oauth2/token` and `/oauth2/jwks` — see section 2 below.

## 1) Create an OIDC application in Asgardeo

1. Sign in to the Asgardeo console for organization **orgfvzwp**.
2. Create an application (e.g. **Single Page Application** with **Authorization Code** + **PKCE**).
3. **Authorized redirect URLs**: `http://localhost:5173/auth/callback`
4. **Post-logout redirect URLs** (if used): `http://localhost:5173`
5. **Allowed origins**: `http://localhost:5173` (needed for browser calls to token/JWKS endpoints).
6. Copy the **Client ID**. Prefer SPA/public client without embedding a client secret in the browser.

## 2) Configure this repo

Update `frontend/.env` (copy from `frontend/.env.example`):

```env
VITE_API_BASE_URL=http://localhost:8000/api
VITE_ASGARDEO_ORG=orgfvzwp
VITE_WSO2_CLIENT_ID=<your-client-id>
VITE_WSO2_REDIRECT_URI=http://localhost:5173/auth/callback
VITE_WSO2_POST_LOGOUT_REDIRECT_URI=http://localhost:5173
```

Update `backend/.env` (copy from `backend/.env.example`):

```env
FRONTEND_ORIGIN=http://localhost:5173
WSO2_ISSUER=https://api.asgardeo.io/t/orgfvzwp/oauth2/token
WSO2_JWKS_URL=https://api.asgardeo.io/t/orgfvzwp/oauth2/jwks
WSO2_AUDIENCE=<your-client-id>
WSO2_VERIFY_TLS=true
```

`WSO2_AUDIENCE` must match the **`aud`** claim on Asgardeo **JWT** access tokens (often your application client ID).

### Backend `/api/cart` returns **401** while the SPA is logged in

Asgardeo may issue **opaque** access tokens (they look like UUIDs, not `eyJ...` JWTs). This API validates opaque tokens by calling Asgardeo’s **token introspection** endpoint using server-side credentials.

Add to **`backend/.env`** (never commit the secret):

```env
ASGARDEO_INTROSPECT_CLIENT_ID=<same-as-your-app-client-id>
ASGARDEO_INTROSPECT_CLIENT_SECRET=<client-secret-from-asgardeo-console>
```

Leave `ASGARDEO_INTROSPECT_CLIENT_ID` empty to reuse `WSO2_AUDIENCE`.

**Alternative:** In Asgardeo, configure the application to issue **JWT** access tokens so the backend can validate with JWKS only (no introspection secret).

If API calls still return 401, decode a JWT access token (if JWT) and align `iss` / `aud` with `WSO2_ISSUER` / `WSO2_AUDIENCE`.

If discovery still returns **404**, the **`orgfvzwp`** segment may not match your real organization name — copy the exact value from the Asgardeo console URL or from your app’s OAuth endpoint examples.

### Token endpoint `POST .../oauth2/token` returns **401** after redirect

Common causes:

1. **Application type** — The client must behave as a **public** SPA: register a **Single Page Application** (Authorization Code + PKCE). A **Traditional Web Application** / confidential client expects a **client secret** on the token request; the browser cannot safely store that secret (and Asgardeo rejects unauthenticated token exchange → **401**).
2. **Library default** — `oidc-client-ts` defaults to `client_secret_post`. This project disables that for SPAs by using **PKCE-only** token posts unless you set `VITE_OIDC_CLIENT_SECRET` (dev-only workaround; secret is embedded in the frontend bundle).

After changing Asgardeo settings or `.env`, restart `npm run dev`.

## 3) Optional: self-hosted WSO2 Identity Server

If you later use local WSO2 IS instead, replace issuer/JWKS with your server URLs (e.g. `https://localhost:9443/oauth2/token`) and set `WSO2_VERIFY_TLS=false` only for self-signed dev certs.
