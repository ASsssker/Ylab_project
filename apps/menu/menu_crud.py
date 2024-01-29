from fastapi import Depends
from sqlalchemy import func, select, distinct
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import FlushError, NoResultFound
from db.db_init import get_session
from uuid import UUID
from .utils import check_unique, check_exist_and_return, obj2dict
from .models import Menu, Submenu, Dish
from .schema import MenuCreate, MenuUpdate


class MenuCrud:
    def __init__(self, db: AsyncSession = Depends(get_session)) -> None:
        self.db = db
        self.model = Menu

    async def get_menu_list(self) -> list[Menu]:
        """Получение списка меню."""
        submenus_count_alias = func.count(distinct(Submenu.id)).label('submenus_count')
        dishes_count_alias = func.count(distinct(Dish.id)).label('dishes_count')
        menus_query = (await self.db.execute(
            select(self.model, submenus_count_alias, dishes_count_alias).join(self.model.submenus, isouter=True)
            .join(Submenu.dishes, isouter=True).group_by(self.model.id)
        )).all()

        menu_list = []
        for menu in menus_query:
            serializer = menu._asdict()
            menu_serializer = obj2dict(serializer['Menu'])
            serializer.update(menu_serializer)
            menu_list.append(serializer)
        return menu_list

    async def get_menu_by_id(self, menu_id: UUID) -> Menu:
        """Поолучение конкретного меню"""
        submenus_count_alias = func.count(distinct(Submenu.id)).label('submenus_count')
        dishes_count_alias = func.count(distinct(Dish.id)).label('dishes_count')
        current_menu = (await self.db.execute(
            select(self.model, submenus_count_alias, dishes_count_alias).
            join(self.model.submenus, isouter=True).join(Submenu.dishes, isouter=True)
            .where(self.model.id == menu_id).group_by(self.model.id)
        )).first()
        if not current_menu:
            raise NoResultFound('menu not found')

        serializer = current_menu._asdict()
        menu_serializer = obj2dict(serializer['Menu'])
        serializer.update(menu_serializer)
        return serializer

    async def create_menu(self, menu: MenuCreate) -> Menu:
        """Добавление нового меню"""
        try:
            await check_unique(db=self.db, obj=menu, model=self.model)
        except FlushError:
            raise FlushError('Такое меню уже существует')
        menu_data = menu.model_dump(exclude_unset=True)
        new_menu = self.model(**menu_data)
        self.db.add(new_menu)
        await self.db.commit()
        await self.db.refresh(new_menu)
        return new_menu

    async def update_menu(self, menu_id: UUID, updated_menu: MenuUpdate) -> Menu:
        """Изменение меню по id."""
        current_menu = await check_exist_and_return(self.db, menu_id, self.model)
        try:
            await check_unique(
                db=self.db,
                obj=updated_menu,
                model=self.model,
                obj_id=menu_id
            )
        except FlushError:
            raise FlushError('Такое меню уже существует')

        menu_data = updated_menu.model_dump(exclude_unset=True)
        for key, value in menu_data.items():
            setattr(current_menu, key, value)
        await self.db.commit()
        await self.db.refresh(current_menu)
        return current_menu

    async def delete(self, menu_id: UUID) -> None:
        """Удаление меню по id"""
        current_menu = await check_exist_and_return(self.db, menu_id, self.model)
        await self.db.delete(current_menu)
        await self.db.commit()
