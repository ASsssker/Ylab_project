from abc import ABC, abstractmethod
from .repository import SQLAlchemyRepository
from .cache_repository import CacheBaseRepository


class AbstractService(ABC):
    @abstractmethod
    async def get_one(self, *args, **kwargs):
        raise NotImplemented

    @abstractmethod
    async def get_all(self, *args, **kwargs):
        raise NotImplemented

    @abstractmethod
    async def add(self, *args, **kwargs):
        raise NotImplemented

    @abstractmethod
    async def update(self, *args, **kwargs):
        raise NotImplemented

    @abstractmethod
    async def delete(self, *args, **kwargs):
        raise NotImplemented


class BaseService(AbstractService):
    def __init__(self, crud_repo: SQLAlchemyRepository, cache_repo: CacheBaseRepository):
        self.crud_repo = crud_repo
        self.cache_repo = cache_repo

    async def get_one(self, *args, **kwargs):
        cache = await self.cache_repo.get(*args, **kwargs)
        if cache:
            return cache
        item = await self.crud_repo.get_record(*args, **kwargs)
        await self.cache_repo.set(item, *args, **kwargs)
        return item

    async def get_all(self, *args, **kwargs):
        cache = await self.cache_repo.get(*args, **kwargs)
        if cache:
            return cache
        item = await self.crud_repo.get_records(*args, **kwargs)
        await self.cache_repo.set(item, *args, **kwargs)
        return item

    async def add(self, *args, **kwargs):
        item = await self.crud_repo.add(*args, **kwargs)
        await self.cache_repo.delete(*args, **kwargs)
        return item

    async def update(self, *args, **kwargs):
        item = await self.crud_repo.update(*args, **kwargs)
        await self.cache_repo.delete_from_pattern(*args, **kwargs)
        return item

    async def delete(self, *args, **kwargs):
        await self.crud_repo.delete(*args, **kwargs)
        await self.cache_repo.delete_from_pattern(*args, **kwargs)

