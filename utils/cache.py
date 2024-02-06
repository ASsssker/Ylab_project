import json
from abc import ABC, abstractmethod
from typing import Any

from aioredis import Redis
from fastapi import Depends

from db.db_init import get_cache


class AbstractCacheRepository(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    async def set_detail(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    async def set_list(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_detail(self, *args, **kwargs) -> dict[str, Any] | None:
        raise NotImplementedError

    @abstractmethod
    async def get_list(self, *args, **kwargs) -> list[dict[str, Any] | None] | None:
        raise NotImplementedError

    @abstractmethod
    async def clear_after_add(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    async def clear_after_update(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    async def clear_all(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    async def set(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete_from_pattern(self, *args, **kwargs) -> None:
        raise NotImplementedError


class CacheBaseRepository(AbstractCacheRepository):
    def __init__(self, cacher: Redis = Depends(get_cache)) -> None:
        self.cacher = cacher

    @abstractmethod
    async def set_detail(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    async def set_list(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_detail(self, *args, **kwargs) -> dict[str, Any] | None:
        raise NotImplementedError

    @abstractmethod
    async def get_list(self, *args, **kwargs) -> list[dict[str, Any] | None] | None:
        raise NotImplementedError

    @abstractmethod
    async def clear_after_add(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    async def clear_after_update(self, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    async def clear_all(self, *args, **kwargs) -> None:
        raise NotImplementedError

    async def set(self, item: dict | list, url: str) -> None:
        await self.cacher.set(
            url,
            json.dumps(item)
        )

    async def delete(self, url: str, *args, **kwargs) -> None:
        await self.cacher.delete(url)

    async def delete_from_pattern(self, url: str, *args, **kwargs) -> None:
        keys = await self.cacher.keys(pattern=url + '*')
        for key in keys:
            await self.cacher.delete(key)
