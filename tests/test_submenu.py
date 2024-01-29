from http import HTTPStatus
from httpx import AsyncClient
from typing import Any
from apps.api.menu_api import post_menu, delete_menu, get_menus
from apps.api.submenu_api import (
    get_submenu,
    get_submenus,
    update_submenu,
    post_submenu,
    delete_submenu
)
from .utils import reverse


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


async def test_submenu_list_is_empty(saved_data: dict[str, str], ac: AsyncClient):
    """Проверка получения пустого списка подменю."""
    menu = saved_data['menu']
    response = await ac.get(reverse(get_submenus, menu_id=menu['id']))
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json() == [], 'В ответе непустой список'


async def test_post_submenu(saved_data: dict[str, str], submenu_post_data: dict[str, str], ac: AsyncClient):
    """Проверка добавления подменю."""
    menu = saved_data['menu']
    response = await ac.post(reverse(post_submenu, menu_id=menu['id']), json=submenu_post_data)
    assert response.status_code == HTTPStatus.CREATED, 'Статус ответа не 201'
    response_data = response.json()
    assert 'id' in response_data, 'Идентификатор подменю отсуствует в ответе'
    assert 'title' in response_data, 'Название подменю отсуствует в ответе'
    assert 'description' in response_data, 'Описание подменю отсуствует в ответе'
    assert 'dishes_count' in response_data, 'Количество блюд отсуствует в ответе'
    assert response_data['title'] == submenu_post_data['title'], 'Название подменю не соответствует ожидаемому'
    assert response_data['description'] == submenu_post_data['description'], 'Описание подменю не соответствует ожидаемому'
    saved_data['submenu'] = response_data


async def test_submenu_list_is_not_empty(saved_data: dict[str, str], ac: AsyncClient):
    """Проверка получения списка подменю после добавления записи."""
    menu = saved_data['menu']
    response = await ac.get(reverse(get_submenus, menu_id=menu['id']))
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json() != [], 'В ответе непустой список'


async def test_get_specific_submenu(saved_data: dict[str, str], ac: AsyncClient):
    """Проверка получения конкретного подменю."""
    menu, submenu = saved_data['menu'], saved_data['submenu']
    response = await ac.get(reverse(get_submenu, menu_id=menu['id'], submenu_id=submenu['id']))
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    response_data = response.json()
    assert 'id' in response_data, 'Идентификатор подменю отсуствует в ответе'
    assert 'title' in response_data, 'Название подменю отсуствует в ответе'
    assert 'description' in response_data, 'Описание подменю отсуствует в ответе'
    assert 'dishes_count' in response_data, 'Количество блюд отсуствует в ответе'
    assert response_data['title'] == submenu['title'], 'Название подменю не соответствует ожидаемому'
    assert response_data['description'] == submenu['description'], 'Описание подменю не соответствует ожидаемому'


async def test_update_submenu(saved_data: dict[str, str], submenu_patch_data, ac: AsyncClient):
    """Проверка обновления подменю."""
    menu, submenu = saved_data['menu'], saved_data['submenu']
    response = await ac.patch(reverse(update_submenu, menu_id=menu['id'], submenu_id=submenu['id']), json=submenu_patch_data)
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    response_data = response.json()
    assert 'id' in response_data, 'Идентификатор подменю отсуствует в ответе'
    assert 'title' in response_data, 'Название подменю отсуствует в ответе'
    assert 'description' in response_data, 'Описание подменю отсуствует в ответе'
    assert 'dishes_count' in response_data, 'Количество блюд отсуствует в ответе'
    assert response_data['title'] == submenu_patch_data['title'], 'Название подменю не соответствует ожидаемому'
    assert response_data['description'] == submenu_patch_data['description'], 'Описание подменю не соответствует ожидаемому'
    saved_data['submenu'] = response_data


async def test_get_updated_menu(saved_data: dict[str, str], ac: AsyncClient):
    """Проверка получения подменю после обновления."""
    menu, submenu = saved_data['menu'], saved_data['submenu']
    response = await ac.get(reverse(get_submenu, menu_id=menu['id'], submenu_id=submenu['id']))
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    response_data = response.json()
    assert 'id' in response_data, 'Идентификатор подменю отсуствует в ответе'
    assert 'title' in response_data, 'Название подменю отсуствует в ответе'
    assert 'description' in response_data, 'Описание подменю отсуствует в ответе'
    assert 'dishes_count' in response_data, 'Количество блюд отсуствует в ответе'
    assert response_data['title'] == submenu['title'], 'Название подменю не соответствует ожидаемому'
    assert response_data['description'] == submenu['description'], 'Описание подменю не соответствует ожидаемому'


async def test_delete_submenu(saved_data: dict[str, str], ac: AsyncClient):
    """Проверка удаления подменю."""
    menu, submenu = saved_data['menu'], saved_data['submenu']
    response = await ac.delete(reverse(delete_submenu, menu_id=menu['id'], submenu_id=submenu['id']))
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'


async def test_submenu_list_is_empty_after_delete(saved_data: dict[str, str], ac: AsyncClient):
    """Проверка получения пустого списка подменю."""
    menu = saved_data['menu']
    response = await ac.get(reverse(get_submenus, menu_id=menu['id']))
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json() == [], 'В ответе непустой список'


async def test_get_specific_submenu_after_delete(saved_data: dict[str, str], ac: AsyncClient):
    """Проверка получения конкретного подменю после удаления."""
    menu, submenu = saved_data['menu'], saved_data['submenu']
    response = await ac.get(reverse(get_submenu, menu_id=menu['id'], submenu_id=submenu['id']))
    assert response.status_code == HTTPStatus.NOT_FOUND, 'Статус ответа не 404'
    assert response.json()['detail'] == 'submenu not found', 'Сообщение об ошибке не соответствует ожидаемому'


async def test_delete_menu(saved_data: dict[str, str], ac: AsyncClient):
    """Проверка удаления данных в меню."""
    menu = saved_data['menu']
    response = await ac.delete(reverse(delete_menu, menu_id=menu['id']))
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'


async def test_all_menu_list_is_empty_after_delete(ac: AsyncClient) -> None:
    """Проверка получения пустого списка меню после удаления меню."""
    response = await ac.get(reverse(get_menus))
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json() == [], 'В ответе непустой список'