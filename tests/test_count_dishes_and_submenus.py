"""
    Проверка кол-ва блюд и подменю в меню
"""
from http import HTTPStatus
from typing import Any

from httpx import AsyncClient

from apps.api.menu.dish_router import post_dish
from apps.api.menu.menu_router import delete_menu, get_menu, get_menus, post_menu
from apps.api.menu.submenu_router import (
    delete_submenu,
    get_submenu,
    get_submenus,
    post_submenu,
)

from .utils import reverse


async def test_post_menu(menu_post_data: dict[str, str], saved_data: dict[str, Any], ac: AsyncClient) -> None:
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


async def test_post_submenu(saved_data: dict[str, Any], submenu_post_data: dict[str, str], ac: AsyncClient):
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


async def test_post_dish_1(dish_post_data_1: dict[str, Any], saved_data: dict[str, Any], ac: AsyncClient):
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
    saved_data['dish_1'] = response_data


async def test_post_dish_2(dish_post_data_2: dict[str, Any], saved_data: dict[str, Any], ac: AsyncClient):
    menu, submenu = saved_data['menu'], saved_data['submenu']
    response = await ac.post(reverse(post_dish, menu_id=menu['id'], submenu_id=submenu['id']), json=dish_post_data_2)
    assert response.status_code == HTTPStatus.CREATED, 'Статус ответа не 201'
    response_data = response.json()
    assert 'id' in response_data, 'Идентификатор блюда отсуствует в ответе'
    assert 'title' in response_data, 'Название бдюда отсуствует в ответе'
    assert 'description' in response_data, 'Описание блюда отсуствует в ответе'
    assert 'price' in response_data, 'Цена блюда отсуствует в ответе'
    assert response_data['title'] == dish_post_data_2['title'], 'Название блюда не соответствует ожидаемому'
    assert response_data['description'] == dish_post_data_2['description'], 'Описание блюда не соответствует ожидаемому'
    assert float(response_data['price']) == round(
        dish_post_data_2['price'], 2), 'Цена блюда не соответствует ожидаемому'
    saved_data['dish_2'] = response_data


async def test_get_specific_menu(saved_data: dict[str, Any], ac: AsyncClient):
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
    assert response_data['submenus_count'] == 1, 'Количество подменю не соответствует ожидаемому'
    assert response_data['dishes_count'] == 2, 'Количество блюд не соответствует ожидаемому'


async def test_get_specific_submenu(saved_data: dict[str, Any], ac: AsyncClient):
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
    assert response_data['dishes_count'] == 2, 'Количество блюд не соответствует ожидаемому'


async def test_delete_submenu(saved_data: dict[str, Any], ac: AsyncClient):
    menu, submenu = saved_data['menu'], saved_data['submenu']
    response = await ac.delete(reverse(delete_submenu, menu_id=menu['id'], submenu_id=submenu['id']))
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'


async def test_submenu_list_is_empty(saved_data: dict[str, Any], ac: AsyncClient):
    menu = saved_data['menu']
    response = await ac.get(reverse(get_submenus, menu_id=menu['id']))
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json() == [], 'В ответе непустой список'


async def test_dish_list_is_empty(saved_data: dict[str, Any], ac: AsyncClient):
    menu, submenu = saved_data['menu'], saved_data['submenu']
    response = await ac.get(reverse(get_submenus, menu_id=menu['id'], submenu_id=submenu['id']))
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json() == [], 'В ответе непустой список'


async def test_get_specific_menu_after_delete(saved_data: dict[str, Any], ac: AsyncClient):
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
    assert response_data['submenus_count'] == 0, 'Количество подменю не соответствует ожидаемому'
    assert response_data['dishes_count'] == 0, 'Количество блюд не соответствует ожидаемому'


async def test_delete_menu(saved_data: dict[str, Any], ac: AsyncClient):
    menu = saved_data['menu']
    response = await ac.delete(reverse(delete_menu, menu_id=menu['id']))
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'


async def test_all_menu_list_is_empty(ac: AsyncClient) -> None:
    response = await ac.get(reverse(get_menus))
    assert response.status_code == HTTPStatus.OK, 'Статус ответа не 200'
    assert response.json() == [], 'В ответе непустой список'
