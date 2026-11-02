from fastapi import FastAPI
from routers import router as api_router

def lifespan(app: FastAPI):
    yield
    
app = FastAPI(title="Library Circulation API", lifespan=lifespan, version="v0.1.0")
app.include_router(api_router)