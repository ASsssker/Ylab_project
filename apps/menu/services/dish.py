from fastapi import Depends
from apps.menu.repositories.dish import DishCrud
from apps.menu.cache.dish import DishCache
from utils.services import BaseService


class DishService(BaseService):
    def __init__(self, crud_repo: DishCrud = Depends(), cache_repo: DishCache = Depends()):
        self.crud_repo = crud_repo
        self.cache_repo = cache_repo

    async def get_one(self, menu_id, submenu_id, dish_id):
        cache = await self.cache_repo.get_detail(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
        if cache:
            return cache
        item = await self.crud_repo.get_record(record_id=dish_id)
        await self.cache_repo.set_detail(item=item, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
        return item

    async def get_all(self, menu_id, submenu_id):
        cache = await self.cache_repo.get_list(menu_id=menu_id, submenu_id=submenu_id)
        if cache:
            return cache
        item = await self.crud_repo.get_records(parent_record_id=submenu_id)
        await self.cache_repo.set_list(item, menu_id=menu_id, submenu_id=submenu_id)
        return item

    async def add(self, model_data, menu_id, submenu_id):
        item = await self.crud_repo.add(submenu_id=submenu_id, model_data=model_data)
        await self.cache_repo.clear_after_add(menu_id=menu_id, submenu_id=submenu_id)
        return item

    async def update(self, menu_id, submenu_id, dish_id, update_data):
        item = await self.crud_repo.update(record_id=dish_id, update_data=update_data)
        await self.cache_repo.clear_after_update(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
        return item

    async def delete(self, menu_id, submenu_id, dish_id):
        await self.crud_repo.delete(record_id=dish_id)
        await self.cache_repo.clear_all(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
