from fastapi import Depends
from utils.cache_repository import CacheBaseRepository
from aioredis import Redis
from db.db_init import get_cache
from apps.api.url_config import MENU_LINK, MENUS_LINK


class MenuCache(CacheBaseRepository):
    def __init__(self, cacher: Redis = Depends(get_cache)):
        self.cacher = cacher
        self.endpoint_list_url = MENUS_LINK
        self.endpoint_detail_url = MENU_LINK

    async def set_detail(self, item, menu_id):
        url = self.endpoint_detail_url.format(menu_id=menu_id)
        await super().set(item=item, url=url)

    async def set_list(self, item):
        url = self.endpoint_list_url
        await super().set(item=item, url=url)

    async def get_detail(self, menu_id):
        url = self.endpoint_detail_url.format(menu_id=menu_id)
        item = await super().get(url=url)
        return item

    async def get_list(self):
        url = self.endpoint_list_url
        item = await super().get(url=url)
        return item

    async def clear_after_add(self):
        url = self.endpoint_list_url
        await self.delete(url=url)

    async def clear_after_update(self, menu_id):
        url_list = self.endpoint_list_url
        url_detail = self.endpoint_detail_url.format(menu_id=menu_id)
        await self.delete(url_list)
        await self.delete(url_detail)

    async def clear_all(self, menu_id):
        list_url = self.endpoint_list_url
        detail_url = self.endpoint_detail_url.format(menu_id=menu_id)
        await self.delete_from_pattern(url=detail_url)
        await self.delete(url=list_url)
