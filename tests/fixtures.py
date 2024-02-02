from typing import Any

import pytest


@pytest.fixture
def menu_post_data() -> dict[str, str]:
    """Фикстура добавления меню"""
    return {
        'title': 'Menu 1',
        'description': 'description 1'
    }


@pytest.fixture
def menu_patch_data() -> dict[str, str]:
    """Фикстура обновления меню"""
    return {
        'title': 'Menu 1 updated',
        'description': 'description 1 updated'
    }


@pytest.fixture
def submenu_post_data() -> dict[str, str]:
    """Фикстура добавления подменю"""
    return {
        'title': 'Submenu 1',
        'description': 'description 1'
    }


@pytest.fixture
def submenu_patch_data() -> dict[str, str]:
    """Фикстура обновления подменю"""
    return {
        'title': 'Submenu 1 updated',
        'description': 'description 1 updated'
    }


@pytest.fixture
def dish_post_data_1() -> dict[str, Any]:
    """Фикстура добавления блюда"""
    return {
        'title': 'Dish 1',
        'description': 'description 1',
        'price': 2222.2222
    }


@pytest.fixture
def dish_post_data_2() -> dict[str, Any]:
    """Фикстура добавления блюда"""
    return {
        'title': 'Dish 2',
        'description': 'description 2',
        'price': 4444.444
    }


@pytest.fixture
def dish_patch_data() -> dict[str, Any]:
    """Фикстура обновления блюда"""
    return {
        'title': 'Dish 1 updated',
        'description': 'description 1 updated',
        'price': 333.33
    }


@pytest.fixture(scope='module')
def saved_data() -> dict[str, Any]:
    """Фикстура для сохранения тестируемых объектов."""
    return {}
