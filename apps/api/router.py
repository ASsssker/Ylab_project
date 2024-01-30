from fastapi import APIRouter
from .menu.menu import menu_router
from .menu.submenu import submenu_router
from .menu.dish import dish_router

api_router = APIRouter()

api_router.include_router(menu_router)
api_router.include_router(submenu_router)
api_router.include_router(dish_router)
