from fastapi import Depends
from sqlalchemy import func, select, distinct
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound
from db.db_init import get_session
from uuid import UUID
from utils.repository import SQLAlchemyRepository
from apps.menu.models import Menu, Submenu, Dish


class MenuCrud(SQLAlchemyRepository):
    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        self.session = session
        self.model = Menu

    async def get_records(self):
        """Получение списка меню."""
        submenus_count_alias = func.count(distinct(Submenu.id)).label('submenus_count')
        dishes_count_alias = func.count(distinct(Dish.id)).label('dishes_count')
        menus_query = (await self.session.execute(
            select(self.model, submenus_count_alias, dishes_count_alias).join(self.model.submenus, isouter=True)
            .join(Submenu.dishes, isouter=True).group_by(self.model.id)
        )).all()

        menu_list = []
        for menu in menus_query:
            serializer = menu._asdict()
            menu_serializer = serializer['Menu'].to_read_mode()
            serializer.update(menu_serializer)
            menu_list.append(serializer)
        return menu_list

    async def get_record(self, record_id: UUID):
        """Поолучение конкретного меню"""
        submenus_count_alias = func.count(distinct(Submenu.id)).label('submenus_count')
        dishes_count_alias = func.count(distinct(Dish.id)).label('dishes_count')
        current_menu = (await self.session.execute(
            select(self.model, submenus_count_alias, dishes_count_alias).
            join(self.model.submenus, isouter=True).join(Submenu.dishes, isouter=True)
            .where(self.model.id == record_id).group_by(self.model.id)
        )).first()
        if not current_menu:
            raise NoResultFound('menu not found')

        serializer = current_menu._asdict()
        menu_serializer = serializer['Menu'].to_read_mode()
        serializer.update(menu_serializer)
        return serializer
