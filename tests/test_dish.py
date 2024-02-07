from http import HTTPStatus
from typing import Any

from httpx import AsyncClient

from apps.api.menu.dish_router import (
    delete_dish,
    get_dish,
    get_dishes,
    post_dish,
    update_dish,
)
from apps.api.menu.menu_router import delete_menu, get_menus, post_menu
from apps.api.menu.submenu_router import delete_submenu, get_submenus, post_submenu

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


async def test_post_submenu(submenu_post_data: dict[str, str], saved_data: dict[str, Any], ac: AsyncClient) -> None:
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


async def test_all_dish_list_is_emty(saved_data: dict[str, Any], ac: AsyncClient) -> None:
    """Проверка получения пустого списка блюд."""
    menu, submenu = saved_data['menu'], saved_data['submenu']
    response = await ac.get(reverse(get_dishes, menu_id=menu['id'], submenu_id=submenu['id']))
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json() == [], 'В ответе непустой список'


async def test_post_dish(dish_post_data_1: dict[str, Any], saved_data: dict[str, Any], ac: AsyncClient) -> None:
    """Проверка добавления блюда."""
    menu, submenu = saved_data['menu'], saved_data['submenu']
    response = await ac.post(reverse(post_dish, menu_id=menu['id'], submenu_id=submenu['id']), json=dish_post_data_1)
    assert response.status_code == HTTPStatus.CREATED, 'Статус ответа не 201'
    response_data = response.json()
    assert 'id' in response_data, 'Идентификатор блюда отсуствует в ответе'
    assert 'title' in response_data, 'Название бдюда отсуствует в ответе'
    assert 'description' in response_data, 'Описание блюда отсуствует в ответе'
    assert 'price' in response_data, 'Цена блюда отсуствует в ответе'
    assert response_data['title'] == dish_post_data_1['title'], 'Название блюда не соответствует ожидаемому'
    assert response_data['description'] == dish_post_data_1['description'], 'Описание блюда не соответствует ожидаемому'
    assert float(response_data['price']) == round(
        dish_post_data_1['price'], 2), 'Цена блюда не соответствует ожидаемому'
    saved_data['dish'] = response_data


async def test_all_dish_list_is_not_empty(saved_data: dict[str, Any], ac: AsyncClient) -> None:
    """Проверка получния списка блюд после добавления записи."""
    menu, submenu = saved_data['menu'], saved_data['submenu']
    response = await ac.get(reverse(get_dishes, menu_id=menu['id'], submenu_id=submenu['id']))
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json() != [], 'В ответе пустой список'


async def test_get_specific_dish(saved_data: dict[str, Any], ac: AsyncClient) -> None:
    """Проверка получение конкретного блюда."""
    menu, submenu, dish = saved_data['menu'], saved_data['submenu'], saved_data['dish']
    response = await ac.get(reverse(get_dish, menu_id=menu['id'], submenu_id=submenu['id'], dish_id=dish['id']))
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    response_data = response.json()
    assert 'id' in response_data, 'Идентификатор блюда отсуствует в ответе'
    assert 'title' in response_data, 'Название бдюда отсуствует в ответе'
    assert 'description' in response_data, 'Описание блюда отсуствует в ответе'
    assert 'price' in response_data, 'Цена блюда отсуствует в ответе'
    assert response_data['title'] == dish['title'], 'Название блюда не соответствует ожидаемому'
    assert response_data['description'] == dish['description'], 'Описание блюда не соответствует ожидаемому'
    assert float(response_data['price']) == float(dish['price']), 'Цена блюда не соответствует ожидаемому'


async def test_update_dish(saved_data: dict[str, Any], dish_patch_data: dict[str, Any], ac: AsyncClient) -> None:
    """Проверка обновления блюда."""
    menu, submenu, dish = saved_data['menu'], saved_data['submenu'], saved_data['dish']
    response = await ac.patch(reverse(update_dish, menu_id=menu['id'], submenu_id=submenu['id'], dish_id=dish['id']), json=dish_patch_data)
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    response_data = response.json()
    assert 'id' in response_data, 'Идентификатор блюда отсуствует в ответе'
    assert 'title' in response_data, 'Название бдюда отсуствует в ответе'
    assert 'description' in response_data, 'Описание блюда отсуствует в ответе'
    assert 'price' in response_data, 'Цена блюда отсуствует в ответе'
    assert response_data['title'] == dish_patch_data['title'], 'Название блюда не соответствует ожидаемому'
    assert response_data['description'] == dish_patch_data['description'], 'Описание блюда не соответствует ожидаемому'
    assert float(response_data['price']) == round(dish_patch_data['price'], 2), 'Цена блюда не соответствует ожидаемому'
    saved_data['dish'] = response_data


async def test_get_updated_menu(saved_data: dict[str, Any], ac: AsyncClient) -> None:
    """Проверка получения обновленного меню"""
    menu, submenu, dish = saved_data['menu'], saved_data['submenu'], saved_data['dish']
    response = await ac.get(reverse(get_dish, menu_id=menu['id'], submenu_id=submenu['id'], dish_id=dish['id']))
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    response_data = response.json()
    assert 'id' in response_data, 'Идентификатор блюда отсуствует в ответе'
    assert 'title' in response_data, 'Название бдюда отсуствует в ответе'
    assert 'description' in response_data, 'Описание блюда отсуствует в ответе'
    assert 'price' in response_data, 'Цена блюда отсуствует в ответе'
    assert response_data['title'] == dish['title'], 'Название блюда не соответствует ожидаемому'
    assert response_data['description'] == dish['description'], 'Описание блюда не соответствует ожидаемому'
    assert float(response_data['price']) == float(dish['price']), 'Цена блюда не соответствует ожидаемому'


async def test_delete_dish(saved_data: dict[str, Any], ac: AsyncClient) -> None:
    """Проверка удаления блюда."""
    menu, submenu, dish = saved_data['menu'], saved_data['submenu'], saved_data['dish']
    response = await ac.delete(reverse(delete_dish, menu_id=menu['id'], submenu_id=submenu['id'], dish_id=dish['id']))
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'


async def test_all_dish_list_is_emty_after_delete(saved_data: dict[str, Any], ac: AsyncClient) -> None:
    """Проверка получения пустого списка блюд после удаления."""
    menu, submenu = saved_data['menu'], saved_data['submenu']
    response = await ac.get(reverse(get_dishes, menu_id=menu['id'], submenu_id=submenu['id']))
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json() == [], 'В ответе непустой список'


async def test_get_specific_dish_after_delete(saved_data: dict[str, Any], ac: AsyncClient) -> None:
    """Проверка получения конкретного блюда после удаления."""
    menu, submenu, dish = saved_data['menu'], saved_data['submenu'], saved_data['dish']
    response = await ac.get(reverse(get_dish, menu_id=menu['id'], submenu_id=submenu['id'], dish_id=dish['id']))
    assert response.status_code == HTTPStatus.NOT_FOUND, 'Статус ответа не 404'
    assert response.json()['detail'] == 'dish not found', 'Сообщение об ошибке не соответствует ожидаемому'


async def test_delete_submenu(saved_data: dict[str, Any], ac: AsyncClient) -> None:
    """Проверка удаления подменю."""
    menu, submenu = saved_data['menu'], saved_data['submenu']
    response = await ac.delete(reverse(delete_submenu, menu_id=menu['id'], submenu_id=submenu['id']))
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'


async def test_submenu_list_is_empty_after_delete(saved_data: dict[str, Any], ac: AsyncClient) -> None:
    """Проверка получения пустого списка подменю."""
    menu = saved_data['menu']
    response = await ac.get(reverse(get_submenus, menu_id=menu['id']))
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json() == [], 'В ответе непустой список'


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
