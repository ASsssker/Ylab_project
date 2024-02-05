from aioredis import Redis
from fastapi import Depends

from apps.api.url_config import MENU_LINK, MENUS_LINK, SUBMENU_LINK, SUBMENUS_LINK
from db.db_init import get_cache
from utils.cache import CacheBaseRepository


class SubmenuCache(CacheBaseRepository):
    def __init__(self, cacher: Redis = Depends(get_cache)) -> None:
        super().__init__(cacher=cacher)
        self.endpoint_list_url: str = SUBMENUS_LINK
        self.endpoint_detail_url: str = SUBMENU_LINK
        self.parent_endpoint_list: str = MENUS_LINK
        self.parent_endpoint_detail: str = MENU_LINK

    async def set_detail(self, item: dict, menu_id: str, submenu_id: str, *args, **kwargs) -> None:
        url = self.endpoint_detail_url.format(menu_id=menu_id, submenu_id=submenu_id)
        await self.set(item=item, url=url)

    async def set_list(self, item: list, menu_id: str, *args, **kwargs) -> None:
        url = self.endpoint_list_url.format(menu_id=menu_id)
        await self.set(item=item, url=url)

    async def get_detail(self, menu_id: str, submenu_id: str, *args, **kwargs) -> list[dict[str, str]] | dict[str, str] | None:
        url = self.endpoint_detail_url.format(menu_id=menu_id, submenu_id=submenu_id)
        item = await self.get(url=url)
        return item

    async def get_list(self, menu_id: str, *args, **kwargs) -> list[dict[str, str]] | dict[str, str] | None:
        url = self.endpoint_list_url.format(menu_id=menu_id)
        item = await self.get(url=url)
        return item

    async def clear_after_add(self, menu_id: str, *args, **kwargs) -> None:
        url_parent_list = self.parent_endpoint_list
        url_parent_detail = self.parent_endpoint_detail.format(menu_id=menu_id)
        url = self.endpoint_list_url.format(menu_id=menu_id)
        await self.delete(url=url)
        await self.delete(url=url_parent_list)
        await self.delete(url=url_parent_detail)

    async def clear_after_update(self, menu_id: str, submenu_id: str, *args, **kwargs) -> None:
        list_url = self.endpoint_list_url.format(menu_id=menu_id)
        detail_url = self.endpoint_detail_url.format(menu_id=menu_id, submenu_id=submenu_id)
        await self.delete(url=list_url)
        await self.delete(url=detail_url)

    async def clear_all(self, menu_id: str, submenu_id: str, *args, **kwargs) -> None:
        parent_list_url = self.parent_endpoint_list
        parent_detail_url = self.parent_endpoint_detail.format(menu_id=menu_id)
        await self.delete_from_pattern(url=parent_detail_url)
        await self.delete(url=parent_list_url)
