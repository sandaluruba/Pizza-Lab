import { Link } from "react-router-dom";
import { useCart } from "../hooks/useCart";

export function CartPage() {
  const { cart, loading, updateItem, removeItem } = useCart();

  if (loading) return <main className="container">Loading cart...</main>;

  return (
    <main className="container">
      <h1>Your Cart</h1>
      {!cart?.items.length && (
        <p>
          Your cart is empty. <Link to="/">Browse pizzas</Link>.
        </p>
      )}
      {cart?.items.map((item) => (
        <article key={item.item_id} className="cart-item">
          <img src={item.thumbnail} alt={item.pizza_name} />
          <div>
            <h3>{item.pizza_name}</h3>
            <p>{item.size_label}</p>
            <p>Rs. {item.line_total.toFixed(2)}</p>
          </div>
          <div className="cart-actions">
            <button onClick={() => void updateItem(item.item_id, Math.max(1, item.quantity - 1))}>
              -
            </button>
            <span>{item.quantity}</span>
            <button onClick={() => void updateItem(item.item_id, item.quantity + 1)}>+</button>
            <button onClick={() => void removeItem(item.item_id)}>Remove</button>
          </div>
        </article>
      ))}
      <h2>Subtotal: Rs. {cart?.subtotal.toFixed(2) ?? "0.00"}</h2>
      <Link className="primary-btn" to="/checkout">
        Continue to checkout
      </Link>
    </main>
  );
}
