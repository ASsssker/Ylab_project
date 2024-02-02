from typing import Callable

from main import app


def get_routes() -> dict[str, str]:
    """Возвращает словарь с url адресами."""
    routes = {}
    for route in app.routes:
        routes[route.name] = route.path
    return routes


def reverse(view: Callable, routes: dict[str, str] = get_routes(), **kwargs) -> str:
    """Возвращает url адрес привязанный к функции представления."""
    return routes[view.__name__].format(**kwargs)
