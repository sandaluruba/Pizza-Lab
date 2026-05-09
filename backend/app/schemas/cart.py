from pydantic import BaseModel, Field


class CartItemInput(BaseModel):
    pizza_id: str
    size_code: str
    quantity: int = Field(ge=1, le=20)


class CartItemUpdate(BaseModel):
    quantity: int = Field(ge=1, le=20)


class CartItemOut(BaseModel):
    item_id: str
    pizza_id: str
    pizza_name: str
    size_code: str
    size_label: str
    unit_price: float
    quantity: int
    line_total: float
    thumbnail: str


class CartOut(BaseModel):
    user_id: str
    items: list[CartItemOut]
    subtotal: float
