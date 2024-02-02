from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.menu.models import Dish
from db.db_init import get_session
from utils.crud import SQLAlchemyCrud


class DishCrud(SQLAlchemyCrud):

    model: type[Dish] = Dish

    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        self.session = session

    async def get_records(self, parent_record_id: str, *args, **kwargs) -> list:
        """Получение списка блюд."""
        dishes_query = (await self.session.execute(
            select(self.model).where(self.model.submenu_id == parent_record_id)
        )).all()
        dish_list = []
        for dish in dishes_query:
            serializer = dish._asdict()
            dish_list.append(serializer['Dish'].to_read_mode())
        return dish_list

    async def add(self, model_data: BaseModel, *args, **kwargs) -> dict:
        current_dish = await super().add(model_data=model_data, submenu_id=kwargs['submenu_id'])
        return current_dish