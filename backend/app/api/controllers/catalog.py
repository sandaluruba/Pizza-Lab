from fastapi import APIRouter, Depends

from app.api.dependencies import get_catalog_service
from app.business.catalog_service import CatalogService
from app.schemas.menu import CategoryOut, PizzaOut

router = APIRouter(prefix="", tags=["catalog"])


@router.get("/categories", response_model=list[CategoryOut])
async def list_categories(service: CatalogService = Depends(get_catalog_service)) -> list[dict]:
    return await service.list_categories()


@router.get("/pizzas", response_model=list[PizzaOut])
async def list_pizzas(
    category: str | None = None,
    service: CatalogService = Depends(get_catalog_service),
) -> list[dict]:
    return await service.list_pizzas(category_id=category)


@router.get("/pizzas/{pizza_id}", response_model=PizzaOut)
async def get_pizza(
    pizza_id: str,
    service: CatalogService = Depends(get_catalog_service),
) -> dict:
    return await service.get_pizza(pizza_id)
