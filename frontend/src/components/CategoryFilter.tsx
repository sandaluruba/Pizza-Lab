import { Category } from "../types/domain";

type Props = {
  categories: Category[];
  selected: string | null;
  onSelect: (categoryId: string | null) => void;
};

export function CategoryFilter({ categories, selected, onSelect }: Props) {
  return (
    <div className="category-row">
      <button
        className={selected === null ? "chip active" : "chip"}
        onClick={() => onSelect(null)}
      >
        All
      </button>
      {categories.map((cat) => (
        <button
          key={cat._id}
          className={selected === cat._id ? "chip active" : "chip"}
          onClick={() => onSelect(cat._id)}
        >
          {cat.name}
        </button>
      ))}
    </div>
  );
}
