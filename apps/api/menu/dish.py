from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.exc import FlushError, NoResultFound
from uuid import UUID
from apps.menu.schema import DishRead, DishUpdate, DishCreate
from apps.api.url_config import PREFIX_LINK, DISHES_LINK, DISH_LINK
from apps.menu.services.dish import DishService


dish_router = APIRouter(prefix=PREFIX_LINK)


@dish_router.get(DISHES_LINK, status_code=200, response_model=list[DishRead])
async def get_dishes(menu_id: UUID, submenu_id: UUID, service: DishService = Depends()) -> list[DishRead]:
    """Получение списка блюд."""
    return await service.get_all(parent_record_id=submenu_id)


@dish_router.post(DISHES_LINK, status_code=201, response_model=DishRead)
async def post_dish(menu_id: UUID, submenu_id: UUID, dish: DishCreate, service: DishService = Depends()) -> DishRead:
    """Добавление нового блюда."""
    try:
        return await service.add(model_data=dish, submenu_id=submenu_id)
    except FlushError as e:
        raise HTTPException(status_code=400, detail=e.args[0])


@dish_router.get(DISH_LINK, status_code=200, response_model=DishRead)
async def get_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID, service: DishService = Depends()) -> DishRead:
    """Получение конкретного блюда."""
    try:
        return await service.get_one(record_id=dish_id)
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail=e.args[0])


@dish_router.patch(DISH_LINK, status_code=200, response_model=DishRead)
async def update_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID, updated_dish: DishUpdate, service: DishService = Depends()) -> DishRead:
    """Изменение блюда по id."""
    try:
        return await service.update(record_id=dish_id, update_data=updated_dish)
    except FlushError as e:
        raise HTTPException(status_code=400, detail=e.args[0])
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail=e.args[0])


@dish_router.delete(DISH_LINK, status_code=200)
async def delete_dish(menu_id: UUID, submenu_id: UUID, dish_id: UUID, service: DishService = Depends()):
    """Удаление блюда по id."""
    try:
        await service.delete(record_id=dish_id)
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail=e.args[0])