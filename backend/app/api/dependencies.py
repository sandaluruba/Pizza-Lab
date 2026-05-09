from app.business.cart_service import CartService
from app.business.catalog_service import CatalogService
from app.business.checkout_service import CheckoutService
from app.core.database import MongoManager
from app.repositories.cart_repository import CartRepository
from app.repositories.catalog_repository import CatalogRepository
from app.repositories.order_repository import OrderRepository


def get_catalog_service() -> CatalogService:
    db = MongoManager.get_db()
    return CatalogService(CatalogRepository(db))


def get_cart_service() -> CartService:
    db = MongoManager.get_db()
    return CartService(
        cart_repository=CartRepository(db),
        catalog_repository=CatalogRepository(db),
    )


def get_checkout_service() -> CheckoutService:
    db = MongoManager.get_db()
    return CheckoutService(
        cart_repository=CartRepository(db),
        order_repository=OrderRepository(db),
    )
