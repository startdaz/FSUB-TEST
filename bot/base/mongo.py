import asyncio
from typing import Any, Dict, List

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError

from ..utils import config, logger


class Database:
    def __init__(self) -> None:
        self.client = None
        self.db = None
        self.db_cache = {}

    async def connect(self) -> None:
        while not self.client:
            try:
                self.client = AsyncIOMotorClient(
                    config.MONGODB_URI, serverSelectionTimeoutMS=5000
                )
                self.db = self.client["FSUB_DATABASE"]["COLLECTIONS"]
                logger.info("MongoDB: Connected")
            except ServerSelectionTimeoutError as e:
                logger.error("MongoDB: Timeout!", exc_info=e)
                self.client = None
                await asyncio.sleep(5)

    async def list_docs(self) -> List[int]:
        pipeline = [{"$project": {"_id": 1}}]
        cursor = self.db.aggregate(pipeline)
        return [document["_id"] async for document in cursor]

    async def get_doc(self, _id: int) -> Dict[str, Any]:
        if _id in self.db_cache:
            return self.db_cache[_id]

        document = await self.db.find_one({"_id": _id})
        if document:
            self.db_cache[_id] = document
        return document

    async def add_value(self, _id: int, key: str, value: Any) -> Dict[str, Any]:
        await self.db.update_one({"_id": _id}, {"$addToSet": {key: value}}, upsert=True)
        if _id in self.db_cache:
            if key not in self.db_cache[_id]:
                self.db_cache[_id][key] = []
            if value not in self.db_cache[_id][key]:
                self.db_cache[_id][key].append(value)
        else:
            self.db_cache[_id] = await self.db.find_one({"_id": _id})
        return self.db_cache[_id]

    async def del_value(self, _id: int, key: str, value: Any) -> None:
        await self.db.update_one({"_id": _id}, {"$pull": {key: value}})
        if _id in self.db_cache:
            if key in self.db_cache[_id]:
                self.db_cache[_id][key] = [
                    v for v in self.db_cache[_id][key] if v != value
                ]

    async def clear_value(self, _id: int, key: str) -> None:
        await self.db.update_one({"_id": _id}, {"$unset": {key: ""}})
        if _id in self.db_cache and key in self.db_cache[_id]:
            del self.db_cache[_id][key]

    async def del_doc(self, _id: int) -> None:
        await self.db.delete_one({"_id": _id})
        if _id in self.db_cache:
            del self.db_cache[_id]


database: Database = Database()
