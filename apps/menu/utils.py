from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import FlushError, NoResultFound
from uuid import UUID
from .models import Menu, Submenu, Dish
from .schema import MenuCreate, SubmenuCreate, DishCreate


async def check_exist_and_return(db: AsyncSession, object_id: UUID, model: [Menu, Submenu, Dish]) -> None:
    """Проверка существования объекта в базе данных."""
    query = select(model).where(model.id == object_id)
    exists_object = await db.scalar(query)
    if not exists_object:
        raise NoResultFound(f'{model.__name__.lower()} not found')
    return exists_object


async def check_unique(
        db: AsyncSession,
        obj: [MenuCreate, SubmenuCreate, DishCreate],
        model: [Menu, Submenu, Dish],
        obj_id: UUID | None = None,
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
    exist_obj = await db.scalar(query)
    if exist_obj:
        raise FlushError


def obj2dict(obj):
    """Преоброзование объекта в словарь"""
    d = {}
    for column in obj.__table__.columns:
        d[column.name] = getattr(obj, column.name)

    return d
