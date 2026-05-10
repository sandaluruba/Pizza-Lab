export type PizzaSize = {
  code: string;
  label: string;
  multiplier: number;
};

export type Category = {
  _id: string;
  name: string;
  description: string;
  thumbnail: string;
};

export type Pizza = {
  _id: string;
  category_id: string;
  name: string;
  description: string;
  image: string;
  thumbnail: string;
  base_price: number;
  sizes: PizzaSize[];
  tags: string[];
};

export type CartItem = {
  item_id: string;
  pizza_id: string;
  pizza_name: string;
  size_code: string;
  size_label: string;
  unit_price: number;
  quantity: number;
  line_total: number;
  thumbnail: string;
};

export type Cart = {
  user_id: string;
  items: CartItem[];
  subtotal: number;
};

export type CheckoutPayload = {
  full_name: string;
  email: string;
  phone: string;
  address: string;
  note?: string;
};
