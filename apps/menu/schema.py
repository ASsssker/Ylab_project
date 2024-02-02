from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Base(BaseModel):
    title: str
    description: str


class MenuRead(Base):
    model_config = ConfigDict(from_attributes=True)
    id: str | UUID
    submenus_count: int | None = None
    dishes_count: int | None = None


class MenuCreate(Base):
    pass


class MenuUpdate(BaseModel):
    title: str | None = None
    description: str | None = None


class SubmenuRead(Base):
    model_config = ConfigDict(from_attributes=True)
    id: str
    menu_id: str
    dishes_count: int | None = None


class SubmenuCreate(Base):
    pass


class SubmenuUpdate(BaseModel):
    title: str | None = None
    description: str | None = None


class DishRead(Base):
    model_config = ConfigDict(from_attributes=True)
    id: str
    submenu_id: str
    price: str | Decimal


class DishCreate(Base):
    price: str | Decimal


class DishUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    price: str | Decimal | None = None
