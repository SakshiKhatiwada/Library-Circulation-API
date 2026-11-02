from fastapi import APIRouter

router = APIRouter(prefix="/lib")

@router.get("/")
def default():
    return {"message": "server running successfully"}