import axios from "axios";
import { Cart, Category, CheckoutPayload, Pizza } from "../types/domain";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
});

const authHeader = (accessToken?: string) =>
  accessToken ? { Authorization: `Bearer ${accessToken}` } : {};

export async function fetchCategories() {
  const { data } = await api.get<Category[]>("/categories");
  return data;
}

export async function fetchPizzas(categoryId?: string) {
  const { data } = await api.get<Pizza[]>("/pizzas", {
    params: categoryId ? { category: categoryId } : undefined,
  });
  return data;
}

export async function fetchPizzaById(pizzaId: string) {
  const { data } = await api.get<Pizza>(`/pizzas/${pizzaId}`);
  return data;
}

export async function fetchCart(accessToken: string) {
  const { data } = await api.get<Cart>("/cart", { headers: authHeader(accessToken) });
  return data;
}

export async function addCartItem(
  accessToken: string,
  payload: { pizza_id: string; size_code: string; quantity: number },
) {
  const { data } = await api.post<Cart>("/cart/items", payload, {
    headers: authHeader(accessToken),
  });
  return data;
}

export async function updateCartItem(
  accessToken: string,
  itemId: string,
  quantity: number,
) {
  const { data } = await api.patch<Cart>(
    `/cart/items/${itemId}`,
    { quantity },
    { headers: authHeader(accessToken) },
  );
  return data;
}

export async function removeCartItem(accessToken: string, itemId: string) {
  const { data } = await api.delete<Cart>(`/cart/items/${itemId}`, {
    headers: authHeader(accessToken),
  });
  return data;
}

export async function checkout(accessToken: string, payload: CheckoutPayload) {
  const { data } = await api.post<{ order_id: string; status: string; total: number }>(
    "/checkout",
    payload,
    {
      headers: authHeader(accessToken),
    },
  );
  return data;
}
