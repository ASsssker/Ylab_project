from fastapi import Depends
from apps.menu.repositories.dish import DishCrud
from utils.services import BaseService


class DishService(BaseService):
    def __init__(self, repo: DishCrud = Depends()):
        self.repo = repo
