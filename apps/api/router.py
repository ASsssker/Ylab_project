from fastapi import APIRouter

from apps.api.menu.dish_router import dish_router
from apps.api.menu.menu_router import menu_router
from apps.api.menu.submenu_router import submenu_router

api_router = APIRouter()

api_router.include_router(menu_router)
api_router.include_router(submenu_router)
api_router.include_router(dish_router)
