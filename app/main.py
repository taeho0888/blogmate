from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app import models
from app.api.api import api_router
from app.database import engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(api_router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
