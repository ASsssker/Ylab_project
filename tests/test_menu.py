from http import HTTPStatus
from typing import Any

from httpx import AsyncClient

from apps.api.menu.menu_router import (
    delete_menu,
    get_menu,
    get_menus,
    post_menu,
    update_menu,
)

from .utils import reverse


async def test_all_menu_list_is_empty(ac: AsyncClient) -> None:
    """Проверка получения пустого списка меню."""
    response = await ac.get(reverse(get_menus))
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json() == [], 'В ответе непустой список'


async def test_post_menu(menu_post_data: dict[str, str], saved_data: dict[str, Any], ac: AsyncClient) -> None:
    """Проверка добавления меню."""
    response = await ac.post(reverse(post_menu), json=menu_post_data)
    assert response.status_code == HTTPStatus.CREATED, 'Статус ответа не 201'
    response_data = response.json()
    assert 'id' in response_data, 'Идентификатор меню отсуствует в ответе'
    assert 'title' in response_data, 'Название меню отсуствует в ответе'
    assert 'description' in response_data, 'Описание меню отсуствует в ответе'
    assert 'submenus_count' in response_data, 'Количество подменю отсуствует в ответе'
    assert 'dishes_count' in response_data, 'Количество блюд отсуствует в ответе'
    assert response_data['title'] == menu_post_data['title'], 'Название меню не соответствует ожидаемому'
    assert response_data['description'] == menu_post_data['description'], 'Описание меню не соответствует ожидаемому'
    saved_data['menu'] = response_data


async def test_all_menu_list_is_not_empty(ac: AsyncClient) -> None:
    """Проверка получения списка меню после добавления записи."""
    response = await ac.get(reverse(get_menus))
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json() != [], 'В ответе пустой список'


async def test_get_specific_menu(saved_data: dict[str, Any], ac: AsyncClient) -> None:
    """Проверка получения конкретного меню."""
    menu = saved_data['menu']
    response = await ac.get(reverse(get_menu, menu_id=menu['id']))
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    response_data = response.json()
    assert 'id' in response_data, 'Идентификатор меню отсуствует в ответе'
    assert 'title' in response_data, 'Название меню отсуствует в ответе'
    assert 'description' in response_data, 'Описание меню отсуствует в ответе'
    assert 'submenus_count' in response_data, 'Количество подменю отсуствует в ответе'
    assert 'dishes_count' in response_data, 'Количество блюд отсуствует в ответе'
    assert response_data['title'] == menu['title'], 'Название меню не соответствует ожидаемому'
    assert response_data['description'] == menu['description'], 'Описание меню не соответствует ожидаемому'


async def test_update_menu(saved_data: dict[str, Any], menu_patch_data: dict[str, str], ac: AsyncClient) -> None:
    """Проверка обновления меню."""
    menu = saved_data['menu']
    response = await ac.patch(reverse(update_menu, menu_id=menu['id']), json=menu_patch_data)
    assert response.status_code == 200, 'Статус ответа не 200'
    response_data = response.json()
    assert 'id' in response_data, 'Идентификатор меню отсуствует в ответе'
    assert 'title' in response_data, 'Название меню отсуствует в ответе'
    assert 'description' in response_data, 'Описание меню отсуствует в ответе'
    assert response_data['title'] == menu_patch_data['title'], 'Название меню не соответствует ожидаемому'
    assert response_data['description'] == \
        menu_patch_data['description'], 'Описание меню не соответствует ожидаемому'
    saved_data['menu'] = response_data


async def test_get_updated_menu(saved_data: dict[str, Any], ac: AsyncClient) -> None:
    """Проверка обновленных данных в меню."""
    menu = saved_data['menu']
    response = await ac.get(reverse(get_menu, menu_id=menu['id']))
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    response_data = response.json()
    assert 'id' in response_data, 'Идентификатор меню отсуствует в ответе'
    assert 'title' in response_data, 'Название меню отсуствует в ответе'
    assert 'description' in response_data, 'Описание меню отсуствует в ответе'
    assert 'submenus_count' in response_data, 'Количество подменю отсуствует в ответе'
    assert 'dishes_count' in response_data, 'Количество блюд отсуствует в ответе'
    assert response_data['title'] == menu['title'], 'Название меню не соответствует ожидаемому'
    assert response_data['description'] == menu['description'], 'Описание меню не соответствует ожидаемому'


async def test_delete_menu(saved_data: dict[str, Any], ac: AsyncClient) -> None:
    """Проверка удаления данных в меню."""
    menu = saved_data['menu']
    response = await ac.delete(reverse(delete_menu, menu_id=menu['id']))
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'


async def test_all_menu_list_is_empty_after_delete(ac: AsyncClient) -> None:
    """Проверка получения пустого списка меню после удаления меню."""
    response = await ac.get(reverse(get_menus))
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json() == [], 'В ответе непустой список'


async def test_get_specific_menu_after_delete(saved_data: dict[str, Any], ac: AsyncClient) -> None:
    """Проверка получение конкретного меню после удаления."""
    menu = saved_data['menu']
    response = await ac.get(reverse(get_menu, menu_id=menu['id']))
    assert response.status_code == HTTPStatus.NOT_FOUND, 'Статус ответа не 404'
    assert response.json()['detail'] == 'menu not found', 'Сообщение об ошибке не соответствует ожидаемому'
