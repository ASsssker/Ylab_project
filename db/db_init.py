from typing import AsyncGenerator

import aioredis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from settings import db_settings


class Base(DeclarativeBase):
    pass


async_engine = create_async_engine(db_settings.database_url_asyncpg)

AsyncSessionLocale = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Возвращает сессию с базой данных."""
    async with AsyncSessionLocale() as async_session:
        yield async_session


async def init_db() -> None:
    """Создание таблиц."""
    async with async_engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)


def init_redis() -> aioredis.Redis:
    return aioredis.from_url(
        db_settings.cache_url,
        encoding='utf8',
        decode_responses=True
    )


redis = init_redis()


def get_cache() -> aioredis.Redis:
    return redis
