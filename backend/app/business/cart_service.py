from uuid import uuid4

from fastapi import HTTPException, status

from app.repositories.cart_repository import CartRepository
from app.repositories.catalog_repository import CatalogRepository


class CartService:
    def __init__(
        self,
        cart_repository: CartRepository,
        catalog_repository: CatalogRepository,
    ) -> None:
        self._cart_repository = cart_repository
        self._catalog_repository = catalog_repository

    async def get_cart(self, user_id: str) -> dict:
        cart = await self._cart_repository.get_cart(user_id)
        return self._compute_totals(user_id, cart.get("items", []))

    async def add_item(self, user_id: str, pizza_id: str, size_code: str, quantity: int) -> dict:
        pizza = await self._catalog_repository.get_pizza_by_id(pizza_id)
        if pizza is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pizza not found.",
            )

        size = next((s for s in pizza["sizes"] if s["code"] == size_code), None)
        if size is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid pizza size.",
            )

        unit_price = round(pizza["base_price"] * size["multiplier"], 2)
        new_item = {
            "item_id": f"itm_{uuid4().hex[:10]}",
            "pizza_id": pizza_id,
            "pizza_name": pizza["name"],
            "size_code": size["code"],
            "size_label": size["label"],
            "unit_price": unit_price,
            "quantity": quantity,
            "thumbnail": pizza["thumbnail"],
        }

        current_cart = await self._cart_repository.get_cart(user_id)
        items = current_cart.get("items", [])
        items.append(new_item)
        await self._cart_repository.upsert_cart(user_id, items)
        return self._compute_totals(user_id, items)

    async def update_item(self, user_id: str, item_id: str, quantity: int) -> dict:
        current_cart = await self._cart_repository.get_cart(user_id)
        items = current_cart.get("items", [])
        matched = False
        for item in items:
            if item["item_id"] == item_id:
                item["quantity"] = quantity
                matched = True
                break
        if not matched:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found.",
            )
        await self._cart_repository.upsert_cart(user_id, items)
        return self._compute_totals(user_id, items)

    async def remove_item(self, user_id: str, item_id: str) -> dict:
        current_cart = await self._cart_repository.get_cart(user_id)
        items = [item for item in current_cart.get("items", []) if item["item_id"] != item_id]
        await self._cart_repository.upsert_cart(user_id, items)
        return self._compute_totals(user_id, items)

    @staticmethod
    def _compute_totals(user_id: str, items: list[dict]) -> dict:
        priced = []
        subtotal = 0.0
        for item in items:
            line_total = round(item["unit_price"] * item["quantity"], 2)
            subtotal += line_total
            priced.append({**item, "line_total": line_total})
        return {"user_id": user_id, "items": priced, "subtotal": round(subtotal, 2)}
