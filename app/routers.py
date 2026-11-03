from fastapi import APIRouter, Depends
from sqlmodel import Session

from db import get_session, SessionDep
from schemas import BookData
from utils import fetch_all_books, upload_books, fetch_one_book

router = APIRouter(prefix="/books")

@router.get("/", status_code=200)
def get_books(session: Session = Depends(get_session)):
    return fetch_all_books(session)

@router.post("", status_code=201)
def post_books(books_info: BookData, session: Session = Depends(get_session)):
    return upload_books(books_info, session)

@router.get("/{book_id}", status_code=200)
def get_book(book_id: int, session: SessionDep):
    return fetch_one_book(book_id, session)