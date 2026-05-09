from fastapi import HTTPException, status

from app.repositories.catalog_repository import CatalogRepository


class CatalogService:
    def __init__(self, repository: CatalogRepository) -> None:
        self._repository = repository

    async def list_categories(self) -> list[dict]:
        return await self._repository.get_categories()

    async def list_pizzas(self, category_id: str | None) -> list[dict]:
        return await self._repository.get_pizzas(category_id=category_id)

    async def get_pizza(self, pizza_id: str) -> dict:
        pizza = await self._repository.get_pizza_by_id(pizza_id)
        if pizza is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pizza not found.",
            )
        return pizza
