import uuid

from sqlalchemy import Column, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.db_init import Base


class Menu(Base):
    """Меню."""
    __tablename__ = 'menus'

    id = Column(
        UUID(as_uuid=False),
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

    def to_read_mode(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description
        }


class Submenu(Base):
    """Подменю."""
    __tablename__ = 'submenus'

    id = Column(
        UUID(as_uuid=False),
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
        UUID(as_uuid=False),
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

    def to_read_mode(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'menu_id': self.menu_id
        }


class Dish(Base):
    """Блюда."""
    __tablename__ = 'dishes'

    id = Column(
        UUID(as_uuid=False),
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
        UUID(as_uuid=False),
        ForeignKey('submenus.id')
    )
    submenu = relationship(
        'Submenu',
        back_populates='dishes'
    )

    def to_read_mode(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'submenu_id': self.submenu_id,
            'price': str(self.price)
        }
