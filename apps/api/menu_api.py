from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.exc import FlushError, NoResultFound
from uuid import UUID
from apps.menu.schema import MenuRead, MenuUpdate, MenuCreate
from apps.menu.menu_crud import MenuCrud
from .url_config import PREFIX_LINK, MENUS_LINK, MENU_LINK


menu_router = APIRouter(prefix=PREFIX_LINK)


@menu_router.get(MENUS_LINK, status_code=200, response_model=list[MenuRead])
async def get_menus(crud: MenuCrud = Depends()) -> list[MenuRead]:
    """Получение списка меню."""
    return await crud.get_menu_list()


@menu_router.post(MENUS_LINK, status_code=201, response_model=MenuRead)
async def post_menu(menu: MenuCreate, crud: MenuCrud = Depends()) -> MenuRead:
    """Добавление нового меню."""
    try:
        return await crud.create_menu(menu=menu)
    except FlushError as e:
        raise HTTPException(status_code=400, detail=e.args[0])


@menu_router.get(MENU_LINK, status_code=200, response_model=MenuRead)
async def get_menu(menu_id: UUID, crud: MenuCrud = Depends()) -> MenuRead:
    """Получение конкретного меню."""
    try:
        return await crud.get_menu_by_id(menu_id=menu_id)
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail=e.args[0])


@menu_router.patch(MENU_LINK, status_code=200, response_model=MenuRead)
async def update_menu(menu_id: UUID, updated_menu: MenuUpdate, crud: MenuCrud = Depends()) -> MenuRead:
    """Изменение меню по id."""
    try:
        return await crud.update_menu(menu_id=menu_id, updated_menu=updated_menu)
    except FlushError as e:
        raise HTTPException(status_code=400, detail=e.args[0])
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail=e.args[0])


@menu_router.delete(MENU_LINK, status_code=200)
async def delete_menu(menu_id: UUID, crud: MenuCrud = Depends()):
    """Удаление меню по id."""
    try:
        await crud.delete(menu_id=menu_id)
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail=e.args[0])