# Authentication Flow (Asgardeo + React + FastAPI)

## How authentication is managed

1. User clicks **Login** in the React app (Asgardeo OIDC).
2. `react-oidc-context` starts OIDC Authorization Code + PKCE flow against Asgardeo (`https://api.asgardeo.io/t/orgfvzwp/oauth2`).
3. Asgardeo authenticates the user and redirects back to `http://localhost:5173/auth/callback?code=...&state=...`.
4. **`AuthProvider` runs `UserManager.signinCallback()`** — this **exchanges the code for tokens** (POST to `/oauth2/token` with `code_verifier`). No custom code is required for that step.
5. After `onSigninCallback` clears the query string, the session (including **`access_token`**) is stored via `oidc-client-ts` (session storage in this project).
6. Cart/checkout calls read **`auth.user.access_token`** and send `Authorization: Bearer <access_token>` to the API (`frontend/src/services/api.ts`, `frontend/src/hooks/useCart.ts`).
7. FastAPI decodes the token using Asgardeo JWKS and validates:
   - `iss` against `WSO2_ISSUER`
   - `aud` against `WSO2_AUDIENCE`
   - signature using public key from `WSO2_JWKS_URL`
8. On valid token, backend extracts `sub` as `user_id` and executes cart/checkout logic.

## Why this design is good for learning

- Frontend shows the full OIDC login lifecycle.
- Backend shows how resource servers validate JWTs from Identity Providers (same pattern as self-hosted WSO2 IS).
- You can inspect issued JWT claims and understand how `iss`, `aud`, and `sub` drive authorization.
