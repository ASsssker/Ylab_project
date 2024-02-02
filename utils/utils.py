from pydantic import BaseModel
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import FlushError, NoResultFound

from db.db_init import Base


async def check_exist_and_return(session: AsyncSession, object_id: str, model: type[Base]) -> Base:
    """Проверка существования объекта в базе данных."""
    query = select(model).where(model.id == object_id)
    exists_object = await session.scalar(query)
    if not exists_object:
        raise NoResultFound(f'{model.__name__.lower()} not found')
    return exists_object


async def check_unique(
        session: AsyncSession,
        obj: BaseModel,
        model: type[Base],
        obj_id: str | None = None,
) -> None:
    """Проверка уникальности объекта"""
    if obj_id:
        """При patch запросе."""
        query = select(exists().where(
            model.title == obj.title,
            model.description == obj.description,
            model.id != obj_id
        ))
    else:
        """При post запросе."""
        query = select(exists().where(
            model.title == obj.title,
            model.description == obj.description
        ))
    exist_obj = await session.scalar(query)
    if exist_obj:
        raise FlushError
