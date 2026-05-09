from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_cart_service
from app.business.cart_service import CartService
from app.core.security import get_current_user
from app.schemas.auth import AuthUser
from app.schemas.cart import CartItemInput, CartItemUpdate, CartOut

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("", response_model=CartOut)
async def get_cart(
    user: AuthUser = Depends(get_current_user),
    service: CartService = Depends(get_cart_service),
) -> dict:
    return await service.get_cart(user.user_id)


@router.post("/items", response_model=CartOut, status_code=status.HTTP_201_CREATED)
async def add_item(
    payload: CartItemInput,
    user: AuthUser = Depends(get_current_user),
    service: CartService = Depends(get_cart_service),
) -> dict:
    return await service.add_item(
        user_id=user.user_id,
        pizza_id=payload.pizza_id,
        size_code=payload.size_code,
        quantity=payload.quantity,
    )


@router.patch("/items/{item_id}", response_model=CartOut)
async def update_item(
    item_id: str,
    payload: CartItemUpdate,
    user: AuthUser = Depends(get_current_user),
    service: CartService = Depends(get_cart_service),
) -> dict:
    return await service.update_item(user.user_id, item_id, payload.quantity)


@router.delete("/items/{item_id}", response_model=CartOut)
async def remove_item(
    item_id: str,
    user: AuthUser = Depends(get_current_user),
    service: CartService = Depends(get_cart_service),
) -> dict:
    return await service.remove_item(user.user_id, item_id)
