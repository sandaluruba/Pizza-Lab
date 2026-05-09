from motor.motor_asyncio import AsyncIOMotorDatabase


class CatalogRepository:
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self._db = db

    async def get_categories(self) -> list[dict]:
        return await self._db.categories.find({}).to_list(length=200)

    async def get_pizzas(self, category_id: str | None = None) -> list[dict]:
        query = {"category_id": category_id} if category_id else {}
        return await self._db.pizzas.find(query).to_list(length=500)

    async def get_pizza_by_id(self, pizza_id: str) -> dict | None:
        return await self._db.pizzas.find_one({"_id": pizza_id})
