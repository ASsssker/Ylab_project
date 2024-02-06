from abc import ABC, abstractmethod
from typing import Any

from utils.cache import CacheBaseRepository
from utils.crud import SQLAlchemyCrud


class AbstractService(ABC):
    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, *args, **kwargs) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, *args, **kwargs) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    async def add(self, *args, **kwargs) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, *args, **kwargs) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, *args, **kwargs) -> None:
        raise NotImplementedError


class BaseService(AbstractService):
    def __init__(self, crud_repo: SQLAlchemyCrud, cache_repo: CacheBaseRepository) -> None:
        self.crud_repo = crud_repo
        self.cache_repo = cache_repo

    async def get_one(self, *args, **kwargs) -> dict[str, Any]:
        cache = await self.cache_repo.get_detail(*args, **kwargs)
        if cache:
            return cache
        item = await self.crud_repo.get_record(*args, **kwargs)
        await self.cache_repo.set_detail(item, *args, **kwargs)
        return item

    async def get_all(self, *args, **kwargs) -> list[dict[str, Any]]:
        cache = await self.cache_repo.get_list(*args, **kwargs)
        if cache:
            return cache
        item = await self.crud_repo.get_records(*args, **kwargs)
        await self.cache_repo.set_list(item, *args, **kwargs)
        return item

    async def add(self, *args, **kwargs) -> dict[str, Any]:
        item = await self.crud_repo.add(*args, **kwargs)
        await self.cache_repo.clear_after_add(*args, **kwargs)
        return item

    async def update(self, *args, **kwargs) -> dict[str, Any]:
        item = await self.crud_repo.update(*args, **kwargs)
        await self.cache_repo.clear_after_update(*args, **kwargs)
        return item

    async def delete(self, *args, **kwargs) -> None:
        await self.crud_repo.delete(*args, **kwargs)
        await self.cache_repo.clear_all(*args, **kwargs)
