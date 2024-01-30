from abc import ABC, abstractmethod
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import FlushError, NoResultFound
from sqlalchemy import select
from uuid import UUID
from db.db_init import Base
from .utils import check_unique, check_exist_and_return


class AbstractRepository(ABC):
    @abstractmethod
    async def get_record(self):
        raise NotImplemented

    @abstractmethod
    async def get_records(self):
        raise NotImplemented

    @abstractmethod
    async def add(self):
        raise NotImplemented

    @abstractmethod
    async def update(self):
        raise NotImplemented

    @abstractmethod
    async def delete(self):
        raise NotImplemented


class SQLAlchemyRepository(AbstractRepository):
    def __init__(self, session: AsyncSession):
        self.model = Base
        self.session = session

    async def get_record(self, id: UUID):
        record = (await self.session.execute(
            select(self.model).where(self.model.id == id)
        )).first()
        if not record:
            raise NoResultFound(f'{self.__class__.__name__.lower()} not found')
        return record

    async def get_records(self):
        records = (await self.session.execute(
            select(self.model).where(self.model.id == id)
        )).all()
        return records

    async def add(self, model_data: BaseModel):
        try:
            await check_unique(
                session=self.session,
                obj=model_data,
                model=self.model
            )
        except FlushError:
            raise FlushError('Такая запись уже существует')
        model_data = model_data.model_dump(exclude_unset=True)
        new_record = self.model(**model_data)
        self.session.add(new_record)
        await self.session.commit()
        await self.session.refresh(new_record)
        return new_record

    async def update(self, record_id: UUID, update_data: BaseModel):
        current_record = await check_exist_and_return(
            session=self.session,
            object_id=record_id,
            model=self.model
        )
        try:
            await check_unique(
                session=self.session,
                obj=update_data,
                model=self.model,
                obj_id=record_id
            )
        except FlushError:
            raise FlushError('Такая запись уже существует')

        update_data = update_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(current_record, key, value)
        await self.session.commit()
        await self.session.refresh(current_record)
        return current_record

    async def delete(self, record_id: UUID):
        current_record = await check_exist_and_return(
            session=self.session,
            object_id=record_id,
            model=self.model
        )
        await self.session.delete(current_record)
        await self.session.commit()
