from pydantic import BaseModel
from decimal import Decimal
from uuid import UUID


class Base(BaseModel):
    title: str
    description: str


class MenuRead(Base):
    id: UUID
    submenus_count: int = 0
    dishes_count: int = 0

    class Config:
        orm_mode = True


class MenuCreate(Base):
    pass


class MenuUpdate(Base):
    title: str = None
    description: str = None


class SubmenuRead(Base):
    id: UUID
    menu_id: UUID
    dishes_count: int = 0

    class Config:
        orm_mode = True


class SubmenuCreate(Base):
    pass


class SubmenuUpdate(Base):
    title: str = None
    description: str = None


class DishRead(Base):
    id: UUID
    submenu_id: UUID
    price: Decimal

    class Config:
        orm_mode = True


class DishCreate(Base):
    price: Decimal


class DishUpdate(Base):
    title: str = None
    description: str = None
    price: Decimal
