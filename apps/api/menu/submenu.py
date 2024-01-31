from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.exc import FlushError, NoResultFound
from uuid import UUID
from apps.menu.schema import SubmenuRead, SubmenuUpdate, SubmenuCreate
from apps.api.url_config import PREFIX_LINK, SUBMENUS_LINK, SUBMENU_LINK
from apps.menu.services.submenu import SubmenuService


submenu_router = APIRouter(prefix=PREFIX_LINK)


@submenu_router.get(SUBMENUS_LINK, status_code=200, response_model=list[SubmenuRead])
async def get_submenus(menu_id: UUID, service: SubmenuService = Depends()) -> list[SubmenuRead]:
    """Получение списка подменю."""
    return await service.get_all(parent_record_id=menu_id)


@submenu_router.post(SUBMENUS_LINK, status_code=201, response_model=SubmenuRead)
async def post_submenu(menu_id: UUID, submenu: SubmenuCreate, service: SubmenuService = Depends()) -> SubmenuRead:
    """Добавление нового подменю."""
    try:
        return await service.add(model_data=submenu, menu_id=menu_id)
    except FlushError as e:
        raise HTTPException(status_code=400, detail=e.args[0])


@submenu_router.get(SUBMENU_LINK, status_code=200, response_model=SubmenuRead)
async def get_submenu(menu_id: UUID, submenu_id: UUID, service: SubmenuService = Depends()) -> SubmenuRead:
    """Получение конкретного подменю."""
    try:
        return await service.get_one(record_id=submenu_id)
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail=e.args[0])


@submenu_router.patch(SUBMENU_LINK, status_code=200, response_model=SubmenuRead)
async def update_submenu(menu_id: UUID, submenu_id: UUID, updated_submenu: SubmenuUpdate, service: SubmenuService = Depends()) -> SubmenuRead:
    """Изменение подменю по id."""
    try:
        return await service.update(record_id=submenu_id, update_data=updated_submenu)
    except FlushError as e:
        raise HTTPException(status_code=400, detail=e.args[0])
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail=e.args[0])


@submenu_router.delete(SUBMENU_LINK, status_code=200)
async def delete_submenu(menu_id: UUID, submenu_id: UUID, service: SubmenuService = Depends()):
    """Удаление подменю по id."""
    try:
        await service.delete(record_id=submenu_id)
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail=e.args[0])
