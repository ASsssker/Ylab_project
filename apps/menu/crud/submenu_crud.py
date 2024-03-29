from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy import distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound

from apps.menu.models import Dish, Menu, Submenu
from db.db_init import get_session
from utils.crud import SQLAlchemyCrud
from utils.utils import check_exist_and_return


class SubmenuCrud(SQLAlchemyCrud):
    def __init__(self, session: AsyncSession = Depends(get_session), model=Submenu) -> None:
        super().__init__(session=session, model=model)

    async def get_records(self, parent_record_id: str, *args, **kwargs) -> list[dict[str, str | int] | None]:
        """Получение списка подменю."""
        submenus_query = (await self.session.execute(
            select(self.model, func.count(distinct(Dish.id)).label('dishes_count'))
            .join(self.model.dishes, isouter=True).where(self.model.menu_id == parent_record_id).group_by(self.model.id)
        )).all()

        submenu_list = []
        for submenu in submenus_query:
            serializer = submenu._asdict()
            submenu_serializer = serializer['Submenu'].to_read_mode()
            del serializer['Submenu']
            serializer.update(submenu_serializer)
            submenu_list.append(serializer)
        return submenu_list

    async def get_record(self, record_id: str, *args, **kwargs) -> dict[str, str | int]:
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
        del serializer['Submenu']
        serializer.update(submenu_serializer)
        return serializer

    async def add(self, model_data: BaseModel, *args, **kwargs) -> dict[str, str]:
        await check_exist_and_return(session=self.session, object_id=kwargs['menu_id'], model=Menu)
        current_submenu = await super().add(model_data=model_data, menu_id=kwargs['menu_id'])
        return current_submenu

    async def update(self, record_id: str, update_data: BaseModel, *args, **kwargs) -> dict[str, str]:
        return await super().update(record_id, update_data, *args, **kwargs)
