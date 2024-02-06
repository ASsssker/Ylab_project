from fastapi import Depends

from apps.menu.cache.menu_cache import MenuCache
from apps.menu.crud.menu_crud import MenuCrud
from apps.menu.schema import MenuCreate, MenuUpdate
from utils.services import BaseService


class MenuService(BaseService):
    def __init__(self, crud_repo: MenuCrud = Depends(), cache_repo: MenuCache = Depends()) -> None:
        super().__init__(crud_repo=crud_repo, cache_repo=cache_repo)

    async def get_one(self, menu_id: str) -> dict[str, str | int]:
        return await super().get_one(record_id=menu_id, menu_id=menu_id)

    async def get_all(self) -> list[dict[str, str | int] | None]:
        return await super().get_all()

    async def add(self, model_data: MenuCreate) -> dict[str, str | int]:
        return await super().add(model_data=model_data)

    async def update(self, menu_id: str, update_data: MenuUpdate) -> dict[str, str]:
        return await super().update(record_id=menu_id, update_data=update_data, menu_id=menu_id)

    async def delete(self, menu_id) -> None:
        await super().delete(record_id=menu_id, menu_id=menu_id)
