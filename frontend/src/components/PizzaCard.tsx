import { Link } from "react-router-dom";
import type { Pizza } from "../types/domain";

type Props = {
  pizza: Pizza;
};

export function PizzaCard({ pizza }: Props) {
  const tags = pizza.tags?.slice(0, 3) ?? [];

  return (
    <article className="pizza-card">
      <div className="pizza-card__media">
        <img src={pizza.thumbnail} alt="" loading="lazy" decoding="async" />
        <span className="pizza-card__media-shine" aria-hidden />
      </div>
      <div className="pizza-card__body">
        <div className="pizza-card__head">
          <h3 className="pizza-card__title">
            <Link to={`/pizza/${pizza._id}`}>{pizza.name}</Link>
          </h3>
          {tags.length > 0 && (
            <ul className="pizza-card__tags" aria-label="Highlights">
              {tags.map((tag) => (
                <li key={tag}>{tag}</li>
              ))}
            </ul>
          )}
        </div>
        <p className="pizza-card__desc">{pizza.description}</p>
        <div className="pizza-card__footer">
          <div className="pizza-card__price">
            <span className="pizza-card__price-label">From</span>
            <span className="pizza-card__price-value">Rs. {pizza.base_price.toFixed(2)}</span>
          </div>
          <Link to={`/pizza/${pizza._id}`} className="pizza-card__cta">
            View & customize
          </Link>
        </div>
      </div>
    </article>
  );
}
