import json
from decimal import Decimal

from aioredis import Redis
from fastapi import Depends

from apps.api.url_config import DISH_LINK, DISHES_LINK, MENU_LINK, MENUS_LINK
from db.db_init import get_cache
from utils.cache import CacheBaseRepository


class DishCache(CacheBaseRepository):
    def __init__(self, cacher: Redis = Depends(get_cache)) -> None:
        super().__init__(cacher=cacher)
        self.endpoint_list_url: str = DISHES_LINK
        self.endpoint_detail_url: str = DISH_LINK
        self.entry_endpoint_list_url: str = MENUS_LINK
        self.entry_endpoint_detail_url: str = MENU_LINK

    async def set_detail(self, item: dict, menu_id: str, submenu_id: str, dish_id: str, *args, **kwargs) -> None:
        url = self.endpoint_detail_url.format(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
        await self.set(item=item, url=url)

    async def set_list(self, item: list, menu_id: str, submenu_id: str, *args, **kwargs) -> None:
        url = self.endpoint_list_url.format(menu_id=menu_id, submenu_id=submenu_id)
        await self.set(item=item, url=url)

    async def get_detail(self, menu_id: str, submenu_id: str, dish_id: str, *args, **kwargs) -> dict[str, str | Decimal] | None:
        url = self.endpoint_detail_url.format(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
        item = await self.cacher.get(url)
        if item:
            return json.loads(item)
        return None

    async def get_list(self, menu_id: str, submenu_id: str, *args, **kwargs) -> list[dict[str, str | Decimal] | None] | None:
        url = self.endpoint_list_url.format(menu_id=menu_id, submenu_id=submenu_id)
        item = await self.cacher.get(url)
        if item:
            return json.loads(item)
        return None

    async def clear_after_add(self, menu_id: str, submenu_id: str, *args, **kwargs) -> None:
        url_entry_list = self.entry_endpoint_list_url
        url_entry_detail = self.entry_endpoint_detail_url.format(menu_id=menu_id)
        await self.delete_from_pattern(url_entry_detail)
        await self.delete(url_entry_list)

    async def clear_after_update(self, menu_id: str, submenu_id: str, dish_id: str, *args, **kwargs) -> None:
        list_url = self.endpoint_list_url.format(menu_id=menu_id, submenu_id=submenu_id)
        detail_url = self.endpoint_detail_url.format(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
        await self.delete_from_pattern(url=list_url)
        await self.delete(url=detail_url)

    async def clear_all(self, menu_id: str, submenu_id: str, dish_id: str, *args, **kwargs) -> None:
        url_entry_list = self.entry_endpoint_list_url
        url_entry_detail = self.entry_endpoint_detail_url.format(menu_id=menu_id)
        await self.delete_from_pattern(url_entry_detail)
        await self.delete(url=url_entry_list)
