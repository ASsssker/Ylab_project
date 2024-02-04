from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    REDIS_HOST: str

    @property
    def database_url_asyncpg(self):
        return f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'

    @property
    def cache_url(self):
        return f'redis://{self.REDIS_HOST}'

    model_config = SettingsConfigDict(env_file='.env.db')


class DatabaseTestSettings(BaseSettings):
    HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    REDIS_HOST: str

    @property
    def database_url_asyncpg(self):
        return f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'

    @property
    def cache_url(self):
        return f'redis://{self.REDIS_HOST}'

    model_config = SettingsConfigDict(env_file='.env.test')


db_settings = DatabaseSettings()
db_test_settings = DatabaseTestSettings()
