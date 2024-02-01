from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_init import get_session
from uuid import UUID
from utils.repository import SQLAlchemyRepository
from apps.menu.models import Dish


class DishCrud(SQLAlchemyRepository):
    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        super().__init__(session)
        self.session = session
        self.model = Dish

    async def get_records(self, parent_record_id: UUID, *args, **kwargs):
        """Получение списка блюд."""
        dishes_query = (await self.session.execute(
            select(self.model).where(self.model.submenu_id == parent_record_id)
        )).all()
        dish_list = []
        for dish in dishes_query:
            serializer = dish._asdict()
            dish_list.append(serializer['Dish'].to_read_mode())
        return dish_list

    async def add(self, model_data: BaseModel, *args, **kwargs):
        current_dish = await super().add(model_data=model_data, submenu_id=kwargs['submenu_id'])
        return current_dish


