from fastapi import HTTPException, status

from app.repositories.cart_repository import CartRepository
from app.repositories.order_repository import OrderRepository


class CheckoutService:
    def __init__(
        self,
        cart_repository: CartRepository,
        order_repository: OrderRepository,
    ) -> None:
        self._cart_repository = cart_repository
        self._order_repository = order_repository

    async def checkout(self, user_id: str, customer: dict) -> dict:
        cart = await self._cart_repository.get_cart(user_id)
        items = cart.get("items", [])
        if not items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot checkout with an empty cart.",
            )

        total = round(sum(item["unit_price"] * item["quantity"] for item in items), 2)
        order = await self._order_repository.create_order(user_id, customer, items, total)
        await self._cart_repository.clear_cart(user_id)
        return order
