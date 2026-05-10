import { useEffect, useState } from "react";
import { CategoryFilter } from "../components/CategoryFilter";
import { PizzaCard } from "../components/PizzaCard";
import { fetchCategories, fetchPizzas } from "../services/api";
import { Category, Pizza } from "../types/domain";

export function MenuPage() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [pizzas, setPizzas] = useState<Pizza[]>([]);

  useEffect(() => {
    void fetchCategories().then(setCategories);
  }, []);

  useEffect(() => {
    void fetchPizzas(selectedCategory ?? undefined).then(setPizzas);
  }, [selectedCategory]);

  return (
    <main className="container">
      <section className="hero">
        <h1>Order hot pizza in minutes</h1>
        <p>Craft your favorite flavor with size options and quick checkout.</p>
      </section>
      <CategoryFilter
        categories={categories}
        selected={selectedCategory}
        onSelect={setSelectedCategory}
      />
      <section className="pizza-grid">
        {pizzas.map((pizza) => (
          <PizzaCard key={pizza._id} pizza={pizza} />
        ))}
      </section>
    </main>
  );
}
