from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from uuid import UUID


class Base(BaseModel):
    title: str
    description: str


class MenuRead(Base):
    model_config = ConfigDict(from_attributes=True)
    id: str | UUID
    submenus_count: int = 0
    dishes_count: int = 0


class MenuCreate(Base):
    pass


class MenuUpdate(Base):
    title: str = None
    description: str = None


class SubmenuRead(Base):
    model_config = ConfigDict(from_attributes=True)
    id: str | UUID
    menu_id: str | UUID
    dishes_count: int = 0


class SubmenuCreate(Base):
    pass


class SubmenuUpdate(Base):
    title: str = None
    description: str = None


class DishRead(Base):
    model_config = ConfigDict(from_attributes=True)
    id: str | UUID
    submenu_id: str | UUID
    price: str | Decimal


class DishCreate(Base):
    price: Decimal


class DishUpdate(Base):
    title: str = None
    description: str = None
    price: Decimal
