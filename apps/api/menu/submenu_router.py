from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.exc import FlushError, NoResultFound

from apps.api.url_config import PREFIX_LINK, SUBMENU_LINK, SUBMENUS_LINK
from apps.menu.schema import SubmenuCreate, SubmenuRead, SubmenuUpdate
from apps.menu.services.submenu_service import SubmenuService

submenu_router = APIRouter(prefix=PREFIX_LINK, tags=['Подменю'])


@submenu_router.get(SUBMENUS_LINK, status_code=status.HTTP_200_OK, response_model=list[SubmenuRead])
async def get_submenus(menu_id: str, service: SubmenuService = Depends()) -> list[dict[str, str | int] | None]:
    """Получение списка подменю."""
    return await service.get_all(menu_id=menu_id)


@submenu_router.post(SUBMENUS_LINK, status_code=status.HTTP_201_CREATED, response_model=SubmenuRead)
async def post_submenu(menu_id: str, submenu: SubmenuCreate, service: SubmenuService = Depends()) -> dict[str, str | int]:
    """Добавление нового подменю."""
    try:
        return await service.add(model_data=submenu, menu_id=menu_id)
    except FlushError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.args[0])
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.args[0])


@submenu_router.get(SUBMENU_LINK, status_code=status.HTTP_200_OK, response_model=SubmenuRead)
async def get_submenu(menu_id: str, submenu_id: str, service: SubmenuService = Depends()) -> dict[str, str | int]:
    """Получение конкретного подменю."""
    try:
        return await service.get_one(menu_id=menu_id, submenu_id=submenu_id)
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.args[0])


@submenu_router.patch(SUBMENU_LINK, status_code=status.HTTP_200_OK, response_model=SubmenuRead, response_model_exclude_none=True)
async def update_submenu(menu_id: str, submenu_id: str, updated_submenu: SubmenuUpdate, service: SubmenuService = Depends()) -> dict[str, str]:
    """Изменение подменю по id."""
    try:
        return await service.update(menu_id=menu_id, submenu_id=submenu_id, update_data=updated_submenu)
    except FlushError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.args[0])
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.args[0])


@submenu_router.delete(SUBMENU_LINK, status_code=status.HTTP_200_OK)
async def delete_submenu(menu_id: str, submenu_id: str, service: SubmenuService = Depends()) -> None:
    """Удаление подменю по id."""
    try:
        await service.delete(menu_id=menu_id, submenu_id=submenu_id)
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.args[0])
