import type { OidcMetadata, UserManagerSettings } from "oidc-client-ts";
import { WebStorageStateStore } from "oidc-client-ts";

/**
 * Asgardeo does not reliably expose OIDC discovery at
 * `{base}/.well-known/openid-configuration` (may 302 to marketing site).
 * We pass explicit metadata so oidc-client-ts skips discovery fetch.
 */
function getOrganizationName(): string {
  const org = import.meta.env.VITE_ASGARDEO_ORG?.trim();
  if (org) return org;
  const legacy = import.meta.env.VITE_WSO2_AUTHORITY?.trim();
  if (legacy) {
    const match = legacy.match(/\/t\/([^/]+)/);
    if (match) return match[1];
  }
  return "orgfvzwp";
}

function buildMetadata(org: string): Partial<OidcMetadata> {
  const base = `https://api.asgardeo.io/t/${org}`;
  const issuer = `${base}/oauth2/token`;
  return {
    issuer,
    authorization_endpoint: `${base}/oauth2/authorize`,
    token_endpoint: `${base}/oauth2/token`,
    jwks_uri: `${base}/oauth2/jwks`,
    userinfo_endpoint: `${base}/oauth2/userinfo`,
    end_session_endpoint: `${base}/oidc/logout`,
  };
}

const organizationName = getOrganizationName();
const metadata = buildMetadata(organizationName);

/**
 * oidc-client-ts defaults to `client_secret_post`, which always appends `client_id` again
 * and assumes a confidential client. Asgardeo **SPA** apps must use PKCE **without** client
 * authentication at the token endpoint.
 *
 * Passing `client_authentication: null` skips that branch so the token POST matches a public client.
 * (Only `undefined` would fall back to the library default — `null` does not.)
 *
 * If your Asgardeo app is **Traditional Web Application** (confidential), set
 * `VITE_OIDC_CLIENT_SECRET` — token endpoint will then use client_secret_post (secret is exposed
 * in the browser bundle; prefer switching to an SPA app or a BFF instead).
 */
const optionalClientSecret = import.meta.env.VITE_OIDC_CLIENT_SECRET?.trim();

export const oidcConfig: UserManagerSettings = {
  authority: metadata.issuer as string,
  metadata,
  client_id: import.meta.env.VITE_WSO2_CLIENT_ID,
  redirect_uri: import.meta.env.VITE_WSO2_REDIRECT_URI,
  post_logout_redirect_uri: import.meta.env.VITE_WSO2_POST_LOGOUT_REDIRECT_URI,
  response_type: "code",
  scope: "openid profile email",
  loadUserInfo: false,
  userStore: new WebStorageStateStore({ store: window.sessionStorage }),
  ...(optionalClientSecret
    ? { client_secret: optionalClientSecret }
    : {
        client_authentication:
          null as unknown as UserManagerSettings["client_authentication"],
      }),
};
