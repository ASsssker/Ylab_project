from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.db_init import init_db
from apps.api.router import api_router

@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(api_router)
