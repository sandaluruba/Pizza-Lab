from pydantic import BaseModel, Field


class CategoryOut(BaseModel):
    id: str = Field(alias="_id")
    name: str
    description: str
    thumbnail: str

    model_config = {"populate_by_name": True}


class PizzaSize(BaseModel):
    code: str
    label: str
    multiplier: float


class PizzaOut(BaseModel):
    id: str = Field(alias="_id")
    category_id: str
    name: str
    description: str
    image: str
    thumbnail: str
    base_price: float
    sizes: list[PizzaSize]
    tags: list[str] = []

    model_config = {"populate_by_name": True}
