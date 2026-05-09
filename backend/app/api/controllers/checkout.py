from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_checkout_service
from app.business.checkout_service import CheckoutService
from app.core.security import get_current_user
from app.schemas.auth import AuthUser
from app.schemas.checkout import CheckoutInput, CheckoutOut

router = APIRouter(prefix="/checkout", tags=["checkout"])


@router.post("", response_model=CheckoutOut, status_code=status.HTTP_201_CREATED)
async def checkout(
    payload: CheckoutInput,
    user: AuthUser = Depends(get_current_user),
    service: CheckoutService = Depends(get_checkout_service),
) -> dict:
    customer = payload.model_dump()
    order = await service.checkout(user.user_id, customer)
    return {"order_id": order["_id"], "status": order["status"], "total": order["total"]}
