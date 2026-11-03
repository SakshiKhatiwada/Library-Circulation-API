from fastapi import FastAPI
from contextlib import asynccontextmanager

from routers.books import router as book_router
from routers.loan import router as loan_router
from db import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    
app = FastAPI(title="Library Circulation API", lifespan=lifespan, version="v0.1.0")
app.include_router(book_router)
app.include_router(loan_router)