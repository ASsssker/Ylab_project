from fastapi import Depends
from apps.menu.repositories.menu import MenuCrud
from utils.services import BaseService


class MenuService(BaseService):
    def __init__(self, repo: MenuCrud = Depends()):
        self.repo = repo
