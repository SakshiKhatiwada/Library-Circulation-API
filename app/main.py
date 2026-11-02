from fastapi import FastAPI
from contextlib import asynccontextmanager

from routers import router as api_router
from db import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    
app = FastAPI(title="Library Circulation API", lifespan=lifespan, version="v0.1.0")
app.include_router(api_router)