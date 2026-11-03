from fastapi import APIRouter, Depends
from sqlmodel import Session

from db import get_session
from schemas import BookData
from utils import fetch_all_books, upload_books

router = APIRouter(prefix="/books")

@router.get("/", status_code=200)
def get_books(session: Session = Depends(get_session)):
    return fetch_all_books(session)

@router.post("/", status_code=201)
def post_books(books_info: BookData, session: Session = Depends(get_session)):
    return upload_books(books_info, session)