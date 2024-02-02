from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.exc import FlushError, NoResultFound

from apps.api.url_config import DISH_LINK, DISHES_LINK, PREFIX_LINK
from apps.menu.schema import DishCreate, DishRead, DishUpdate
from apps.menu.services.dish_service import DishService

dish_router = APIRouter(prefix=PREFIX_LINK)


@dish_router.get(DISHES_LINK, status_code=200, response_model=list[DishRead])
async def get_dishes(menu_id: str, submenu_id: str, service: DishService = Depends()) -> list:
    """Получение списка блюд."""
    return await service.get_all(menu_id=menu_id, submenu_id=submenu_id)


@dish_router.post(DISHES_LINK, status_code=201, response_model=DishRead)
async def post_dish(menu_id: str, submenu_id: str, dish: DishCreate, service: DishService = Depends()) -> dict:
    """Добавление нового блюда."""
    try:
        return await service.add(model_data=dish, menu_id=menu_id, submenu_id=submenu_id)
    except FlushError as e:
        raise HTTPException(status_code=400, detail=e.args[0])


@dish_router.get(DISH_LINK, status_code=200, response_model=DishRead)
async def get_dish(menu_id: str, submenu_id: str, dish_id: str, service: DishService = Depends()) -> dict:
    """Получение конкретного блюда."""
    try:
        return await service.get_one(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail=e.args[0])


@dish_router.patch(DISH_LINK, status_code=200, response_model=DishRead)
async def update_dish(menu_id: str, submenu_id: str, dish_id: str, updated_dish: DishUpdate, service: DishService = Depends()) -> dict:
    """Изменение блюда по id."""
    try:
        return await service.update(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id, update_data=updated_dish)
    except FlushError as e:
        raise HTTPException(status_code=400, detail=e.args[0])
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail=e.args[0])


@dish_router.delete(DISH_LINK, status_code=200)
async def delete_dish(menu_id: str, submenu_id: str, dish_id: str, service: DishService = Depends()) -> None:
    """Удаление блюда по id."""
    try:
        await service.delete(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail=e.args[0])
