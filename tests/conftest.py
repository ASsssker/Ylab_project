import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from db.db_init import Base, get_session
from main import app
from settings import db_test_settings

pytest_plugins = 'tests.fixtures'


engine_test = create_async_engine(
    db_test_settings.database_url_asyncpg,
    poolclass=NullPool
)
AsyncSessionLocale = async_sessionmaker(
    engine_test,
    class_=AsyncSession,
    expire_on_commit=False
)
Base.metadata.bind = engine_test


async def ovveride_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Возвращает сессию с базой данных связанную с тестовым движком."""
    async with AsyncSessionLocale() as session:
        yield session

app.dependency_overrides[get_session] = ovveride_get_async_session


@pytest.fixture(scope='session', autouse=True)
async def prepare_database() -> AsyncGenerator[None, None]:
    """Создает тестовую базу данных."""
    async with engine_test.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as connect:
        await connect.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def ac():
    """Возвращает асинхронный клиент."""
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac
