from fastapi import Depends
from sqlalchemy import func, select, distinct
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound
from db.db_init import get_session
from uuid import UUID
from utils.repository import SQLAlchemyRepository
from .models import Submenu, Dish


class SubmenuCrud(SQLAlchemyRepository):
    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        self.session = session
        self.model = Submenu

    async def get_records(self, parent_record_id: UUID):
        """Получение списка подменю."""
        submenus_query = (await self.session.execute(
            select(self.model, func.count(distinct(Dish.id)).label('dishes_count'))
            .join(self.model.dishes, isouter=True).where(self.model.menu_id == parent_record_id).group_by(self.model.id)
        )).all()

        submenu_list = []
        for submenu in submenus_query:
            serializer = submenu._asdict()
            submenu_serializer = serializer['Submenu'].to_read_mode()
            serializer.update(submenu_serializer)
            submenu_list.append(serializer)
        return submenu_list

    async def get_record(self, record_id: UUID):
        """Поолучение конкретного подменю."""
        current_submenu = (await self.session.execute(
            select(self.model, func.count(distinct(Dish.id)).label('dishes_count'))
            .join(self.model.dishes, isouter=True).where(self.model.id == record_id)
            .group_by(self.model.id)
        )).first()
        if not current_submenu:
            raise NoResultFound('submenu not found')

        serializer = current_submenu._asdict()
        submenu_serializer = serializer['Submenu'].to_read_mode()
        serializer.update(submenu_serializer)
        return serializer

