import { Route, Routes } from "react-router-dom";
import { AppHeader } from "./components/AppHeader";
import { useCart } from "./hooks/useCart";
import { AuthCallbackPage } from "./pages/AuthCallbackPage";
import { CartPage } from "./pages/CartPage";
import { CheckoutPage } from "./pages/CheckoutPage";
import { MenuPage } from "./pages/MenuPage";
import { OrderSuccessPage } from "./pages/OrderSuccessPage";
import { PizzaDetailsPage } from "./pages/PizzaDetailsPage";

export default function App() {
  const { cart } = useCart();

  return (
    <>
      <AppHeader cartCount={cart?.items.length ?? 0} />
      <Routes>
        <Route path="/" element={<MenuPage />} />
        <Route path="/pizza/:pizzaId" element={<PizzaDetailsPage />} />
        <Route path="/cart" element={<CartPage />} />
        <Route path="/checkout" element={<CheckoutPage />} />
        <Route path="/auth/callback" element={<AuthCallbackPage />} />
        <Route path="/order-success" element={<OrderSuccessPage />} />
      </Routes>
    </>
  );
}
