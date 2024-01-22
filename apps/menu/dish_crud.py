from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import FlushError, NoResultFound
from db.db_init import get_db
from uuid import UUID
from .utils import check_unique, check_exist_and_return
from .models import Dish
from .schema import DishCreate, DishUpdate


class DishCrud:
    def __init__(self, db: AsyncSession = Depends(get_db)) -> None:
        self.db = db
        self.model = Dish

    async def get_dish_list(self, submenu_id: UUID) -> list[Dish]:
        """Получение списка блюд."""
        return await self.db.scalars(select(self.model).where(self.model.submenu_id == submenu_id))

    async def get_dish_by_id(self, dish_id: UUID) -> Dish:
        """Поолучение конкретного блюда."""
        current_dish = await self.db.scalar(select(self.model).where(self.model.id == dish_id))
        if not current_dish:
            raise NoResultFound('dish not found')

        return current_dish

    async def create_dish(self, submenu_id: UUID, dish: DishCreate) -> Dish:
        """Добавление нового блюда."""
        try:
            await check_unique(db=self.db, obj=dish, model=self.model)
        except FlushError:
            raise FlushError('Такое блюдо уже существует')
        dish_data = dish.model_dump(exclude_unset=True)
        new_dish = self.model(submenu_id=submenu_id, **dish_data)
        self.db.add(new_dish)
        await self.db.commit()
        await self.db.refresh(new_dish)
        return new_dish

    async def update_dish(self, dish_id: UUID, updated_dish: DishUpdate) -> Dish:
        """Изменение подменю по id."""
        current_dish = await check_exist_and_return(self.db, dish_id, self.model)
        try:
            await check_unique(
                db=self.db,
                obj=updated_dish,
                model=self.model,
                obj_id=dish_id
            )
        except FlushError:
            raise FlushError('Такое блюдо уже существует')

        dish_data = updated_dish.model_dump(exclude_unset=True)
        for key, value in dish_data.items():
            setattr(current_dish, key, value)
        await self.db.commit()
        await self.db.refresh(current_dish)
        return current_dish

    async def delete(self, dish_id: UUID) -> None:
        """Удаление блюда по id."""
        current_dish = await check_exist_and_return(self.db, dish_id, self.model)
        await self.db.delete(current_dish)
        await self.db.commit()
