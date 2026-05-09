from datetime import UTC, datetime
from uuid import uuid4

from motor.motor_asyncio import AsyncIOMotorDatabase


class OrderRepository:
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self._db = db

    async def create_order(
        self,
        user_id: str,
        customer: dict,
        items: list[dict],
        total: float,
    ) -> dict:
        order_id = f"ord_{uuid4().hex[:10]}"
        record = {
            "_id": order_id,
            "user_id": user_id,
            "customer": customer,
            "items": items,
            "total": total,
            "status": "PLACED",
            "created_at": datetime.now(UTC).isoformat(),
        }
        await self._db.orders.insert_one(record)
        return record
