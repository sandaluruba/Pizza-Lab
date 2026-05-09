from motor.motor_asyncio import AsyncIOMotorDatabase


class CartRepository:
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self._db = db

    async def get_cart(self, user_id: str) -> dict:
        cart = await self._db.carts.find_one({"_id": user_id})
        if cart:
            return cart
        return {"_id": user_id, "items": []}

    async def upsert_cart(self, user_id: str, items: list[dict]) -> dict:
        await self._db.carts.update_one(
            {"_id": user_id},
            {"$set": {"items": items}},
            upsert=True,
        )
        return {"_id": user_id, "items": items}

    async def clear_cart(self, user_id: str) -> None:
        await self._db.carts.update_one({"_id": user_id}, {"$set": {"items": []}}, upsert=True)
