from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.exc import FlushError, NoResultFound

from apps.api.menu.api_response_information import MENU_NOT_FOUND, VALUE_IS_EXIST
from apps.api.url_config import MENU_LINK, MENUS_LINK, PREFIX_LINK
from apps.menu.schema import MenuCreate, MenuRead, MenuUpdate
from apps.menu.services.menu_service import MenuService

menu_router = APIRouter(prefix=PREFIX_LINK, tags=['Меню'])


@menu_router.get(MENUS_LINK,
                 summary='Получить все меню',
                 status_code=status.HTTP_200_OK,
                 response_model=list[MenuRead])
async def get_menus(service: MenuService = Depends()) -> list[dict[str, str | int] | None]:
    """Получение списка меню."""
    return await service.get_all()


@menu_router.post(MENUS_LINK,
                  summary='Добавить меню',
                  status_code=status.HTTP_201_CREATED,
                  response_model=MenuRead,
                  responses=VALUE_IS_EXIST)
async def post_menu(menu: MenuCreate, service: MenuService = Depends()) -> dict[str, str | int]:
    """Добавление нового меню."""
    try:
        return await service.add(model_data=menu)
    except FlushError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.args[0])


@menu_router.get(MENU_LINK,
                 summary='Получить меню',
                 status_code=status.HTTP_200_OK,
                 response_model=MenuRead,
                 responses=MENU_NOT_FOUND)
async def get_menu(menu_id: str, service: MenuService = Depends()) -> dict[str, str | int]:
    """Получение конкретного меню."""
    try:
        return await service.get_one(menu_id=menu_id)
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.args[0])


@menu_router.patch(MENU_LINK,
                   summary='Обновть меню',
                   status_code=status.HTTP_200_OK,
                   response_model=MenuRead,
                   response_model_exclude_none=True,
                   responses={**MENU_NOT_FOUND, **VALUE_IS_EXIST})
async def update_menu(menu_id: str, updated_menu: MenuUpdate, service: MenuService = Depends()) -> dict[str, str]:
    """Изменение меню по id."""
    try:
        return await service.update(menu_id=menu_id, update_data=updated_menu)
    except FlushError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.args[0])
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.args[0])


@menu_router.delete(MENU_LINK,
                    summary='Удалить меню',
                    status_code=status.HTTP_200_OK,
                    responses=MENU_NOT_FOUND)
async def delete_menu(menu_id: str, service: MenuService = Depends()) -> None:
    """Удаление меню по id."""
    try:
        await service.delete(menu_id=menu_id)
    except NoResultFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.args[0])
