import { Link, NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "react-oidc-context";

type Props = {
  cartCount: number;
};

export function AppHeader({ cartCount }: Props) {
  const auth = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    void auth.removeUser().then(() => navigate("/", { replace: true }));
  };

  return (
    <header className="topbar">
      <Link className="brand" to="/">
        Pizza Lab
      </Link>
      <nav>
        <NavLink to="/" className="nav-link">
          Menu
        </NavLink>
        <NavLink to="/cart" className="nav-link">
          Cart ({cartCount})
        </NavLink>
        <NavLink to="/checkout" className="nav-link">
          Checkout
        </NavLink>
      </nav>
      <div className="auth-actions">
        {auth.isAuthenticated ? (
          <button type="button" className="btn-auth btn-auth-outline" onClick={handleLogout}>
            Log out
          </button>
        ) : (
          <button type="button" className="btn-auth btn-auth-primary" onClick={() => void auth.signinRedirect()}>
            Login
          </button>
        )}
      </div>
    </header>
  );
}
