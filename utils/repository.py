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
    def __init__(self):
        pass

    @abstractmethod
    async def get_record(self, *args, **kwargs):
        raise NotImplemented

    @abstractmethod
    async def get_records(self, *args, **kwargs):
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


class SQLAlchemyRepository(AbstractRepository):
    def __init__(self, session: AsyncSession):
        self.model = Base
        self.session = session

    async def get_record(self, record_id: UUID, *args, **kwargs):
        record = (await self.session.execute(
            select(self.model).where(self.model.id == record_id)
        )).scalar_one_or_none()
        if not record:
            raise NoResultFound(f'{self.model.__name__.lower()} not found')
        return record.to_read_mode()

    async def get_records(self, *args, **kwargs):
        records = (await self.session.execute(
            select(self.model).where(self.model.id == id)
        )).scalars()

        record_list = []
        for record in records:
            serializer = record._asdict()
            record_list.append(serializer[f'{self.model.__name__}'].to_read_mode())
        return record_list

    async def add(self, model_data: BaseModel, *args, **kwargs):
        try:
            await check_unique(
                session=self.session,
                obj=model_data,
                model=self.model
            )
        except FlushError:
            raise FlushError('Такая запись уже существует')
        model_data = model_data.model_dump(exclude_unset=True)
        new_record = self.model(**model_data, **kwargs)
        self.session.add(new_record)
        await self.session.commit()
        await self.session.refresh(new_record)
        return new_record.to_read_mode()

    async def update(self, record_id: UUID, update_data: BaseModel, *args, **kwargs):
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
        return current_record.to_read_mode()

    async def delete(self, record_id: UUID, *args, **kwargs):
        current_record = await check_exist_and_return(
            session=self.session,
            object_id=record_id,
            model=self.model
        )
        await self.session.delete(current_record)
        await self.session.commit()
