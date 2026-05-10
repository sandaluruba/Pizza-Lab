import { FormEvent, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "react-oidc-context";
import { checkout } from "../services/api";

export function CheckoutPage() {
  const auth = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({
    full_name: "",
    email: "",
    phone: "",
    address: "",
    note: "",
  });

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    const token = auth.user?.access_token;
    if (!token) {
      await auth.signinRedirect();
      return;
    }
    const result = await checkout(token, form);
    navigate(`/order-success?orderId=${result.order_id}`);
  };

  return (
    <main className="container">
      <h1>Checkout</h1>
      <form className="checkout-form" onSubmit={submit}>
        <input
          placeholder="Full name"
          required
          value={form.full_name}
          onChange={(e) => setForm({ ...form, full_name: e.target.value })}
        />
        <input
          type="email"
          placeholder="Email"
          required
          value={form.email}
          onChange={(e) => setForm({ ...form, email: e.target.value })}
        />
        <input
          placeholder="Phone"
          required
          value={form.phone}
          onChange={(e) => setForm({ ...form, phone: e.target.value })}
        />
        <textarea
          placeholder="Delivery address"
          required
          value={form.address}
          onChange={(e) => setForm({ ...form, address: e.target.value })}
        />
        <textarea
          placeholder="Order note (optional)"
          value={form.note}
          onChange={(e) => setForm({ ...form, note: e.target.value })}
        />
        <button className="primary-btn" type="submit">
          Place order
        </button>
      </form>
    </main>
  );
}
