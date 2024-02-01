from fastapi import Depends
from apps.menu.repositories.menu import MenuCrud
from apps.menu.cache.menu import MenuCache
from utils.services import BaseService


class MenuService(BaseService):
    def __init__(self, crud_repo: MenuCrud = Depends(), cache_repo: MenuCache = Depends()):
        self.crud_repo = crud_repo
        self.cache_repo = cache_repo

    async def get_one(self, menu_id):
        cache = await self.cache_repo.get_detail(menu_id=menu_id)
        if cache:
            return cache
        item = await self.crud_repo.get_record(record_id=menu_id)
        await self.cache_repo.set_detail(item=item, menu_id=menu_id)
        return item

    async def get_all(self):
        cache = await self.cache_repo.get_list()
        if cache:
            return cache
        item = await self.crud_repo.get_records()
        await self.cache_repo.set_list(item)
        return item

    async def add(self, model_data):
        item = await self.crud_repo.add(model_data=model_data)
        await self.cache_repo.clear_after_add()
        return item

    async def update(self, menu_id, update_data):
        item = await self.crud_repo.update(record_id=menu_id, update_data=update_data)
        await self.cache_repo.clear_after_update(menu_id=menu_id)
        return item

    async def delete(self, menu_id):
        await self.crud_repo.delete(record_id=menu_id)
        await self.cache_repo.clear_all(menu_id=menu_id)

