from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_init import get_session
from uuid import UUID
from utils.repository import SQLAlchemyRepository
from .models import Dish


class DishCrud(SQLAlchemyRepository):
    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        self.session = session
        self.model = Dish

    async def get_records(self, parent_record_id: UUID):
        """Получение списка блюд."""
        dishes_query = (await self.session.execute(
            select(self.model).where(self.model.submenu_id == parent_record_id)
        )).scalars()

        return dishes_query

