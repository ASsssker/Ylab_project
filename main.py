from fastapi import FastAPI
from db.db_init import init_db
from apps.api.main_api import api_router


app = FastAPI()


@app.on_event('startup')
async def on_startup():
    await init_db()

app.include_router(api_router)
