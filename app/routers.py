from fastapi import APIRouter
from db import get_session

router = APIRouter(prefix="/lib")

@router.get("/")
def default():
    return {"message": "server running successfully"}