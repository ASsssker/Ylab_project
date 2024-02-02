from fastapi import Depends

from apps.menu.cache.submenu_cache import SubmenuCache
from apps.menu.crud.submenu_crud import SubmenuCrud
from apps.menu.schema import SubmenuCreate, SubmenuUpdate
from utils.services import BaseService


class SubmenuService(BaseService):
    def __init__(self, crud_repo: SubmenuCrud = Depends(), cache_repo: SubmenuCache = Depends()) -> None:
        self.crud_repo = crud_repo
        self.cache_repo = cache_repo

    async def get_one(self, menu_id: str, submenu_id: str) -> dict:
        return await super().get_one(record_id=submenu_id, menu_id=menu_id, submenu_id=submenu_id)

    async def get_all(self, menu_id: str) -> list:
        return await super().get_all(parent_record_id=menu_id, menu_id=menu_id)

    async def add(self, model_data: SubmenuCreate, menu_id: str) -> dict:
        return await super().add(menu_id=menu_id, model_data=model_data)

    async def update(self, menu_id: str, submenu_id: str, update_data: SubmenuUpdate) -> dict:
        return await super().update(record_id=submenu_id, update_data=update_data, menu_id=menu_id, submenu_id=submenu_id)

    async def delete(self, menu_id: str, submenu_id: str) -> None:
        await super().delete(record_id=submenu_id, menu_id=menu_id, submenu_id=submenu_id)
