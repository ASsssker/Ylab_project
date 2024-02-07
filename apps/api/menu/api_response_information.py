VALUE_IS_EXIST = {
    400: {
        'description': 'Value already exists',
        'content': {
            'application/json': {
                'example': 'value already exists'
            }
        }
    }
}

MENU_NOT_FOUND = {
    404: {
        'description': 'Menu not found',
        'content': {
            'application/json': {
                'example': 'menu not found'
            }
        }
    }
}


SUBMENU_NOT_FOUND = {
    404: {
        'description': 'Submenu not found',
        'content': {
            'application/json': {
                'example': 'submenu not found'
            }
        }
    }
}

DISH_NOT_FOUND = {
    404: {
        'description': 'Dish not found',
        'content': {
            'application/json': {
                'example': 'dish not found'
            }
        }
    }
}
