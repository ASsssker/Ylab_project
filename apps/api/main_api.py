from fastapi import APIRouter
from .menu_api import menu_router
from .submenu_api import submenu_router
from .dish_api import dish_router

api_router = APIRouter()

api_router.include_router(menu_router)
api_router.include_router(submenu_router)
api_router.include_router(dish_router)
