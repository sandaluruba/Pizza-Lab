from pydantic import BaseModel


class AuthUser(BaseModel):
    user_id: str
    username: str | None = None
    email: str | None = None
