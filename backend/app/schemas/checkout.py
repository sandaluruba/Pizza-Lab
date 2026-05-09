from pydantic import BaseModel, EmailStr, Field


class CheckoutInput(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(min_length=7, max_length=20)
    address: str = Field(min_length=5, max_length=300)
    note: str | None = Field(default=None, max_length=300)


class CheckoutOut(BaseModel):
    order_id: str
    status: str
    total: float
