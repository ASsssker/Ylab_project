import asyncio
import pytest
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from httpx import AsyncClient
from db.db_init import Base, get_session
from main import app
from settings import db_test_settings


pytest_plugins = ('tests.fixtures', 'tests.test_submenu')


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
async def prepare_database() -> None:
    """Создает тестовую базу данных."""
    async with engine_test.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as connect:
        await connect.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='module')
def event_loop():
    """Создает цикл событий для каждого тестового модуля."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def ac():
    """Возвращает асинхронный клиент."""
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac
