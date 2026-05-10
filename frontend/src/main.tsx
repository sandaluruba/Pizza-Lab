import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { AuthProvider } from "react-oidc-context";
import type { User } from "oidc-client-ts";
import App from "./App";
import { oidcConfig } from "./auth/oidc";
import "./styles/app.css";

/** After redirect login, strip ?code=&state= so sign-in is not processed twice (React Strict Mode). */
function onSigninCallback(_user: User | void): void {
  window.history.replaceState({}, document.title, window.location.pathname);
}

ReactDOM.createRoot(document.getElementById("app") as HTMLElement).render(
  <React.StrictMode>
    <AuthProvider {...oidcConfig} onSigninCallback={onSigninCallback}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </AuthProvider>
  </React.StrictMode>,
);
