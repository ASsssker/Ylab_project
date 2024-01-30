from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.exc import FlushError, NoResultFound
from uuid import UUID
from apps.menu.schema import SubmenuRead, SubmenuUpdate, SubmenuCreate
from apps.menu.submenu_crud import SubmenuCrud
from .url_config import PREFIX_LINK, SUBMENUS_LINK, SUBMENU_LINK


submenu_router = APIRouter(prefix=PREFIX_LINK)


@submenu_router.get(SUBMENUS_LINK, status_code=200, response_model=list[SubmenuRead])
async def get_submenus(menu_id: UUID, crud: SubmenuCrud = Depends()) -> list[SubmenuRead]:
    """Получение списка подменю."""
    return await crud.get_records(parent_record_id=menu_id)


@submenu_router.post(SUBMENUS_LINK, status_code=201, response_model=SubmenuRead)
async def post_submenu(menu_id: UUID, submenu: SubmenuCreate, crud: SubmenuCrud = Depends()) -> SubmenuRead:
    """Добавление нового подменю."""
    try:
        return await crud.add(model_data=submenu, menu_id=menu_id)
    except FlushError as e:
        raise HTTPException(status_code=400, detail=e.args[0])


@submenu_router.get(SUBMENU_LINK, status_code=200, response_model=SubmenuRead)
async def get_submenu(menu_id: UUID, submenu_id: UUID, crud: SubmenuCrud = Depends()) -> SubmenuRead:
    """Получение конкретного подменю."""
    try:
        return await crud.get_record(record_id=submenu_id)
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail=e.args[0])


@submenu_router.patch(SUBMENU_LINK, status_code=200, response_model=SubmenuRead)
async def update_submenu(menu_id: UUID, submenu_id: UUID, updated_submenu: SubmenuUpdate, crud: SubmenuCrud = Depends()) -> SubmenuRead:
    """Изменение подменю по id."""
    try:
        return await crud.update(record_id=submenu_id, update_data=updated_submenu)
    except FlushError as e:
        raise HTTPException(status_code=400, detail=e.args[0])
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail=e.args[0])


@submenu_router.delete(SUBMENU_LINK, status_code=200)
async def delete_submenu(menu_id: UUID, submenu_id: UUID, crud: SubmenuCrud = Depends()):
    """Удаление подменю по id."""
    try:
        await crud.delete(record_id=submenu_id)
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail=e.args[0])
