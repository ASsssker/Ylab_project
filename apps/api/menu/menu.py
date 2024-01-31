from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.exc import FlushError, NoResultFound
from uuid import UUID
from apps.menu.schema import MenuRead, MenuUpdate, MenuCreate
from apps.api.url_config import PREFIX_LINK, MENUS_LINK, MENU_LINK
from apps.menu.services.menu import MenuService


menu_router = APIRouter(prefix=PREFIX_LINK)


@menu_router.get(MENUS_LINK, status_code=200, response_model=list[MenuRead])
async def get_menus(service: MenuService = Depends()) -> list[MenuRead]:
    """Получение списка меню."""
    return await service.get_all()


@menu_router.post(MENUS_LINK, status_code=201, response_model=MenuRead)
async def post_menu(menu: MenuCreate, service: MenuService = Depends()) -> MenuRead:
    """Добавление нового меню."""
    try:
        return await service.add(model_data=menu)
    except FlushError as e:
        raise HTTPException(status_code=400, detail=e.args[0])


@menu_router.get(MENU_LINK, status_code=200, response_model=MenuRead)
async def get_menu(menu_id: UUID, service: MenuService = Depends()) -> MenuRead:
    """Получение конкретного меню."""
    try:
        return await service.get_one(record_id=menu_id)
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail=e.args[0])


@menu_router.patch(MENU_LINK, status_code=200, response_model=MenuRead)
async def update_menu(menu_id: UUID, updated_menu: MenuUpdate, service: MenuService = Depends()) -> MenuRead:
    """Изменение меню по id."""
    try:
        return await service.update(record_id=menu_id, update_data=updated_menu)
    except FlushError as e:
        raise HTTPException(status_code=400, detail=e.args[0])
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail=e.args[0])


@menu_router.delete(MENU_LINK, status_code=200)
async def delete_menu(menu_id: UUID, service: MenuService = Depends()):
    """Удаление меню по id."""
    try:
        await service.delete(record_id=menu_id)
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail=e.args[0])
