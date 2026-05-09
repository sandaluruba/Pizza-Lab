from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.controllers import auth, cart, catalog, checkout
from app.core.config import get_settings
from app.core.database import MongoManager

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    MongoManager.connect()
    yield
    MongoManager.close()


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(catalog.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(cart.router, prefix="/api")
app.include_router(checkout.router, prefix="/api")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
