import { useCallback, useEffect, useState } from "react";
import { useAuth } from "react-oidc-context";
import {
  addCartItem,
  fetchCart,
  removeCartItem,
  updateCartItem,
} from "../services/api";
import { Cart } from "../types/domain";

export function useCart() {
  const auth = useAuth();
  const token = auth.user?.access_token;
  const [cart, setCart] = useState<Cart | null>(null);
  const [loading, setLoading] = useState(false);

  const refresh = useCallback(async () => {
    if (!token) {
      setCart(null);
      return;
    }
    setLoading(true);
    try {
      const data = await fetchCart(token);
      setCart(data);
    } finally {
      setLoading(false);
    }
  }, [token]);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  const addItem = async (pizzaId: string, sizeCode: string, quantity: number) => {
    if (!token) return null;
    const data = await addCartItem(token, {
      pizza_id: pizzaId,
      size_code: sizeCode,
      quantity,
    });
    setCart(data);
    return data;
  };

  const updateItem = async (itemId: string, quantity: number) => {
    if (!token) return null;
    const data = await updateCartItem(token, itemId, quantity);
    setCart(data);
    return data;
  };

  const removeItem = async (itemId: string) => {
    if (!token) return null;
    const data = await removeCartItem(token, itemId);
    setCart(data);
    return data;
  };

  return { cart, loading, refresh, addItem, updateItem, removeItem };
}
