import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "react-oidc-context";

/**
 * OAuth redirects here with ?code=&state=. AuthProvider runs UserManager.signinCallback()
 * (authorization_code + PKCE → access_token) before children render. We navigate away once
 * loading finishes — see src/main.tsx onSigninCallback to remove query params from the URL.
 */
export function AuthCallbackPage() {
  const auth = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (auth.isLoading) return;
    if (auth.error) return;
    if (auth.isAuthenticated) {
      navigate("/", { replace: true });
    }
  }, [auth.isLoading, auth.isAuthenticated, auth.error, navigate]);

  if (auth.error) {
    return (
      <main className="container">
        <h1>Sign-in failed</h1>
        <p>{auth.error.message ?? String(auth.error)}</p>
      </main>
    );
  }

  return <main className="container">Completing login…</main>;
}
