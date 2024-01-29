from fastapi import Depends
from sqlalchemy import func, select, distinct
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import FlushError, NoResultFound
from db.db_init import get_session
from uuid import UUID
from .utils import check_unique, check_exist_and_return, obj2dict
from .models import Submenu, Dish
from .schema import SubmenuCreate, SubmenuUpdate


class SubmenuCrud:
    def __init__(self, db: AsyncSession = Depends(get_session)) -> None:
        self.db = db
        self.model = Submenu

    async def get_submenu_list(self, menu_id: UUID) -> list[Submenu]:
        """Получение списка подменю."""
        submenus_query = (await self.db.execute(
            select(self.model, func.count(distinct(Dish.id)).label('dishes_count'))
            .join(self.model.dishes, isouter=True).where(self.model.menu_id == menu_id).group_by(self.model.id)
        )).all()

        submenu_list = []
        for submenu in submenus_query:
            serializer = submenu._asdict()
            submenu_serializer = obj2dict(serializer['Submenu'])
            serializer.update(submenu_serializer)
            submenu_list.append(serializer)
        return submenu_list

    async def get_submenu_by_id(self, submenu_id: UUID) -> Submenu:
        """Поолучение конкретного подменю."""
        current_submenu = (await self.db.execute(
            select(self.model, func.count(distinct(Dish.id)).label('dishes_count'))
            .join(self.model.dishes, isouter=True).where(self.model.id == submenu_id)
            .group_by(self.model.id)
        )).first()
        if not current_submenu:
            raise NoResultFound('submenu not found')

        serializer = current_submenu._asdict()
        submenu_serializer = obj2dict(serializer['Submenu'])
        serializer.update(submenu_serializer)
        return serializer

    async def create_submenu(self, menu_id: UUID, submenu: SubmenuCreate) -> Submenu:
        """Добавление нового подменю."""
        try:
            await check_unique(db=self.db, obj=submenu, model=self.model)
        except FlushError:
            raise FlushError('Такое подменю уже существует')
        submenu_data = submenu.model_dump(exclude_unset=True)
        new_submenu = self.model(menu_id=menu_id, **submenu_data)
        self.db.add(new_submenu)
        await self.db.commit()
        await self.db.refresh(new_submenu)
        return new_submenu

    async def update_submenu(self, submenu_id: UUID, updated_submenu: SubmenuUpdate) -> Submenu:
        """Изменение подменю по id."""
        current_submenu = await check_exist_and_return(self.db, submenu_id, self.model)
        try:
            await check_unique(
                db=self.db,
                obj=updated_submenu,
                model=self.model,
                obj_id=submenu_id
            )
        except FlushError:
            raise FlushError('Такое подменю уже существует')

        submenu_data = updated_submenu.model_dump(exclude_unset=True)
        for key, value in submenu_data.items():
            setattr(current_submenu, key, value)
        await self.db.commit()
        await self.db.refresh(current_submenu)
        return current_submenu

    async def delete(self, submenu_id: UUID) -> None:
        """Удаление подменю по id."""
        current_submenu = await check_exist_and_return(self.db, submenu_id, self.model)
        await self.db.delete(current_submenu)
        await self.db.commit()
