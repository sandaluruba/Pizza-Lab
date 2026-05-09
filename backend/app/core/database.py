from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import get_settings


class MongoManager:
    client: AsyncIOMotorClient | None = None
    db: AsyncIOMotorDatabase | None = None

    @classmethod
    def connect(cls) -> None:
        settings = get_settings()
        cls.client = AsyncIOMotorClient(settings.mongo_uri)
        cls.db = cls.client[settings.mongo_db]

    @classmethod
    def close(cls) -> None:
        if cls.client:
            cls.client.close()
        cls.client = None
        cls.db = None

    @classmethod
    def get_db(cls) -> AsyncIOMotorDatabase:
        if cls.db is None:
            raise RuntimeError("Database is not connected.")
        return cls.db
