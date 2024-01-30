import uuid
from sqlalchemy import Column, ForeignKey, String, Text, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db.db_init import Base
from .schema import MenuRead, SubmenuRead, DishRead


class Menu(Base):
    """Меню."""
    __tablename__ = 'menus'

    id = Column(
        UUID(),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    title = Column(
        String(length=50),
        nullable=False
    )
    description = Column(
        Text(),
        nullable=False
    )
    submenus = relationship(
        'Submenu',
        back_populates='menu',
        cascade='all, delete'
    )

    def to_read_mode(self) -> MenuRead:
        return MenuRead(
            id=self.id,
            title=self.title,
            description=self.description
        )


class Submenu(Base):
    """Подменю."""
    __tablename__ = 'submenus'

    id = Column(
        UUID(),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    title = Column(
        String(length=50),
        nullable=False
    )
    description = Column(
        Text(),
        nullable=False
    )
    menu_id = Column(
        UUID(),
        ForeignKey('menus.id')
    )
    menu = relationship(
        'Menu',
        back_populates='submenus'
    )
    dishes = relationship(
        'Dish',
        back_populates='submenu',
        cascade='all, delete'
    )

    def to_read_mode(self) -> SubmenuRead:
        return SubmenuRead(
            id=self.id,
            title=self.title,
            description=self.description
        )


class Dish(Base):
    """Блюда."""
    __tablename__ = 'dishes'

    id = Column(
        UUID(),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    title = Column(
        String(length=50),
        nullable=False
    )
    description = Column(
        Text(),
        nullable=False
    )
    price = Column(
        Numeric(12, 2),
        nullable=False
    )
    submenu_id = Column(
        UUID(),
        ForeignKey('submenus.id')
    )
    submenu = relationship(
        'Submenu',
        back_populates='dishes'
    )

    def to_read_mode(self) -> DishRead:
        return DishRead(
            id=self.id,
            title=self.title,
            description=self.description
        )
