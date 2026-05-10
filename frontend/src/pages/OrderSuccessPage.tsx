import { useMemo } from "react";
import { Link, useLocation } from "react-router-dom";

export function OrderSuccessPage() {
  const location = useLocation();
  const orderId = useMemo(
    () => new URLSearchParams(location.search).get("orderId") ?? "N/A",
    [location.search],
  );

  return (
    <main className="container">
      <h1>Order placed!</h1>
      <p>Your order id is {orderId}.</p>
      <p>Our kitchen has started preparing your pizza.</p>
      <Link className="primary-btn" to="/">
        Back to menu
      </Link>
    </main>
  );
}
