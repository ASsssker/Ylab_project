from abc import ABC, abstractmethod
from .repository import AbstractRepository


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
    def __init__(self, repo: AbstractRepository):
        self.repo = repo

    async def get_one(self, *args, **kwargs):
        return await self.repo.get_record(*args, **kwargs)

    async def get_all(self, *args, **kwargs):
        return await self.repo.get_records(*args, **kwargs)

    async def add(self, *args, **kwargs):
        return await self.repo.add(*args, **kwargs)

    async def update(self, *args, **kwargs):
        return await self.repo.update(*args, **kwargs)

    async def delete(self, *args, **kwargs):
        return await self.repo.delete(*args, **kwargs)

