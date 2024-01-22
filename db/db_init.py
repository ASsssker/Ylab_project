from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from settings import db_settings

Base = declarative_base()
async_engine = create_async_engine(db_settings.database_url_asyncpg)

AsyncSessionLocale = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession
)


async def get_db():
    """Возвращает сессию с базой данных."""
    async with AsyncSessionLocale() as async_session:
        yield async_session


async def init_db():
    """Создание таблиц."""
    async with async_engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)
