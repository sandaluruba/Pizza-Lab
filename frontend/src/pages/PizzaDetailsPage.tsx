import { useEffect, useMemo, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useAuth } from "react-oidc-context";
import { useCart } from "../hooks/useCart";
import { fetchPizzaById } from "../services/api";
import { Pizza } from "../types/domain";

export function PizzaDetailsPage() {
  const { pizzaId = "" } = useParams();
  const auth = useAuth();
  const navigate = useNavigate();
  const { addItem } = useCart();
  const [pizza, setPizza] = useState<Pizza | null>(null);
  const [sizeCode, setSizeCode] = useState("S");
  const [quantity, setQuantity] = useState(1);

  useEffect(() => {
    void fetchPizzaById(pizzaId).then((data) => {
      setPizza(data);
      setSizeCode(data.sizes[0]?.code ?? "S");
    });
  }, [pizzaId]);

  const selectedSize = useMemo(
    () => pizza?.sizes.find((size) => size.code === sizeCode),
    [pizza, sizeCode],
  );
  const total = useMemo(() => {
    if (!pizza || !selectedSize) return 0;
    return pizza.base_price * selectedSize.multiplier * quantity;
  }, [pizza, selectedSize, quantity]);

  const handleAdd = async () => {
    if (!pizza) return;
    if (!auth.isAuthenticated) {
      await auth.signinRedirect();
      return;
    }
    await addItem(pizza._id, sizeCode, quantity);
    navigate("/cart");
  };

  if (!pizza) return <main className="container">Loading pizza...</main>;

  return (
    <main className="container details-layout">
      <img className="details-image" src={pizza.image} alt={pizza.name} />
      <section>
        <h1>{pizza.name}</h1>
        <p>{pizza.description}</p>
        <div className="size-group">
          {pizza.sizes.map((size) => (
            <button
              key={size.code}
              className={size.code === sizeCode ? "chip active" : "chip"}
              onClick={() => setSizeCode(size.code)}
            >
              {size.label}
            </button>
          ))}
        </div>
        <div className="quantity-row">
          <button onClick={() => setQuantity((q) => Math.max(1, q - 1))}>-</button>
          <span>{quantity}</span>
          <button onClick={() => setQuantity((q) => q + 1)}>+</button>
        </div>
        <h3>Total: Rs. {total.toFixed(2)}</h3>
        <button className="primary-btn" onClick={handleAdd}>
          Add to cart
        </button>
      </section>
    </main>
  );
}
