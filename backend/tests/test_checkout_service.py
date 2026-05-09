import pytest
from fastapi import HTTPException

from app.business.checkout_service import CheckoutService


class FakeCartRepo:
    async def get_cart(self, _: str):
        return {"_id": "u1", "items": []}

    async def clear_cart(self, _: str):
        return None


class FakeOrderRepo:
    async def create_order(self, user_id: str, customer: dict, items: list, total: float):
        return {
            "_id": "ord_123",
            "user_id": user_id,
            "customer": customer,
            "items": items,
            "total": total,
            "status": "PLACED",
        }


@pytest.mark.asyncio
async def test_checkout_throws_for_empty_cart():
    service = CheckoutService(FakeCartRepo(), FakeOrderRepo())

    with pytest.raises(HTTPException) as exc:
        await service.checkout("u1", {"full_name": "A"})

    assert exc.value.status_code == 400
