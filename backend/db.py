import os
from motor.motor_asyncio import AsyncIOMotorClient

_client: AsyncIOMotorClient | None = None


def get_client() -> AsyncIOMotorClient:
    if _client is None:
        raise RuntimeError("Database not connected — call connect() first")
    return _client


def get_db():
    return get_client()[os.environ["MONGO_DB"]]


async def connect():
    global _client
    _client = AsyncIOMotorClient(os.environ["MONGO_URI"])
    # Verify the connection is live on startup
    await _client.admin.command("ping")


async def close():
    global _client
    if _client:
        _client.close()
        _client = None
