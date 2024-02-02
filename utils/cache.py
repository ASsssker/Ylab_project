import json
from abc import ABC, abstractmethod

from aioredis import Redis
from fastapi import Depends

from db.db_init import get_cache


class AbstactCacheRepository(ABC):
    @abstractmethod
    def set(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def get(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def delete(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def delete_from_pattern(self, *args, **kwargs):
        raise NotImplementedError


class CacheBaseRepository(AbstactCacheRepository):
    def __init__(self, cacher: Redis = Depends(get_cache)):
        self.cacher = cacher

    @abstractmethod
    async def set_detail(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def set_list(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_detail(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_list(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def clear_after_add(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def clear_after_update(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def clear_all(self, *args, **kwargs):
        raise NotImplementedError

    async def set(self, item: dict | list, url: str) -> None:
        await self.cacher.set(
            url,
            json.dumps(item)
        )

    async def get(self, url: str) -> list[dict[str, str]] | dict[str, str] | None:
        cache = await self.cacher.get(url)
        if cache:
            return json.loads(cache)

        return None

    async def delete(self, url: str) -> None:
        await self.cacher.delete(url)

    async def delete_from_pattern(self, url: str) -> None:
        keys = await self.cacher.keys(pattern=url + '*')
        for key in keys:
            await self.cacher.delete(key)
