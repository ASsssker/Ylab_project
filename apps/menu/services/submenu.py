from fastapi import Depends
from apps.menu.repositories.submenu import SubmenuCrud
from utils.services import BaseService


class SubmenuService(BaseService):
    def __init__(self, repo: SubmenuCrud = Depends()):
        self.repo = repo
