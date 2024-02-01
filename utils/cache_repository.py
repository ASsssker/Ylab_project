import json
from fastapi import Request
from abc import ABC, abstractmethod
from aioredis import Redis
from fastapi import Depends
from db.db_init import get_cache


class AbstactCacheRepository(ABC):
    @abstractmethod
    def set(self, *args, **kwargs):
        raise NotImplemented

    @abstractmethod
    def get(self, *args, **kwargs):
        raise NotImplemented

    @abstractmethod
    def delete(self, *args, **kwargs):
        raise NotImplemented

    @abstractmethod
    def delete_from_pattern(self, *args, **kwargs):
        raise NotImplemented


class CacheBaseRepository(AbstactCacheRepository):
    def __init__(self, cacher: Redis = Depends(get_cache)):
        self.cacher = cacher

    async def set(self, item: dict, url: str):
        await self.cacher.set(
            url,
            json.dumps(item)
        )

    async def get(self, url: str):
        cache = await self.cacher.get(url)
        if cache:
            return json.loads(cache)

        return None

    async def delete(self, url: str):
        await self.cacher.delete(url)

    async def delete_from_pattern(self, url: str):
        keys = await self.cacher.keys(pattern=url + '*')
        for key in keys:
            await self.cacher.delete(key)
