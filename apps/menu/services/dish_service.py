from decimal import Decimal

from fastapi import Depends

from apps.menu.cache.dish_cache import DishCache
from apps.menu.crud.dish_crud import DishCrud
from apps.menu.schema import DishCreate, DishUpdate
from utils.services import BaseService


class DishService(BaseService):
    def __init__(self, crud_repo: DishCrud = Depends(), cache_repo: DishCache = Depends()) -> None:
        super().__init__(crud_repo=crud_repo, cache_repo=cache_repo)

    async def get_one(self, menu_id: str, submenu_id: str, dish_id: str) -> dict[str, str | Decimal]:
        return await super().get_one(record_id=dish_id, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)

    async def get_all(self, menu_id: str, submenu_id: str) -> list[dict[str, str | Decimal] | None]:
        return await super().get_all(parent_record_id=submenu_id, menu_id=menu_id, submenu_id=submenu_id)

    async def add(self, model_data: DishCreate, menu_id: str, submenu_id: str) -> dict[str, str | Decimal]:
        return await super().add(model_data=model_data, menu_id=menu_id, submenu_id=submenu_id)

    async def update(self, menu_id: str, submenu_id: str, dish_id: str, update_data: DishUpdate) -> dict[str, str | Decimal]:
        return await super().update(record_id=dish_id, update_data=update_data, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)

    async def delete(self, menu_id: str, submenu_id: str, dish_id: str) -> None:
        await super().delete(record_id=dish_id, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
