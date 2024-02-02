from contextlib import asynccontextmanager

from fastapi import FastAPI

from apps.api.router import api_router
from db.db_init import init_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(api_router)
