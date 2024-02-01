import asyncio
from fastapi import Depends
from utils.cache_repository import CacheBaseRepository
from aioredis import Redis
from db.db_init import get_cache
from apps.api.url_config import SUBMENU_LINK, SUBMENUS_LINK, MENUS_LINK, MENU_LINK, DISH_LINK, DISHES_LINK


class DishCache(CacheBaseRepository):
    def __init__(self, cacher: Redis = Depends(get_cache)):
        self.cacher = cacher
        self.endpoint_list_url = DISHES_LINK
        self.endpoint_detail_url = DISH_LINK
        self.entry_endpoint_list_url = MENUS_LINK
        self.entry_endpoint_detail_url = MENU_LINK
        self.urls = [DISH_LINK, DISHES_LINK, SUBMENUS_LINK, SUBMENU_LINK, MENU_LINK, MENUS_LINK]

    async def set_detail(self, item, menu_id, submenu_id, dish_id):
        url = self.endpoint_detail_url.format(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
        await self.set(item=item, url=url)

    async def set_list(self, item, menu_id, submenu_id):
        url = self.endpoint_list_url.format(menu_id=menu_id, submenu_id=submenu_id)
        await self.set(item=item, url=url)

    async def get_detail(self, menu_id, submenu_id, dish_id):
        url = self.endpoint_detail_url.format(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
        item = await self.get(url=url)
        return item

    async def get_list(self, menu_id, submenu_id):
        url = self.endpoint_list_url.format(menu_id=menu_id, submenu_id=submenu_id)
        item = await self.get(url=url)
        return item

    async def clear_after_add(self, menu_id, submenu_id):
        url_entry_list= self.entry_endpoint_list_url
        url_entry_detail = self.entry_endpoint_detail_url.format(menu_id=menu_id)
        await self.delete_from_pattern(url_entry_detail)
        await self.delete(url_entry_list)


    async def clear_after_update(self, menu_id, submenu_id, dish_id):
        list_url = self.endpoint_list_url.format(menu_id=menu_id, submenu_id=submenu_id)
        detail_url = self.endpoint_detail_url.format(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
        await self.delete_from_pattern(url=list_url)
        await self.delete(url=detail_url)

    async def clear_all(self, menu_id, submenu_id, dish_id):
        url_entry_list = self.entry_endpoint_list_url
        url_entry_detail = self.entry_endpoint_detail_url.format(menu_id=menu_id)
        await self.delete_from_pattern(url_entry_detail)
        await self.delete(url=url_entry_list)
