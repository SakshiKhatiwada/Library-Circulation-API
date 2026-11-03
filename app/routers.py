from fastapi import APIRouter, Depends
from sqlmodel import Session

from db import get_session, SessionDep
from schemas import BookData, BookUpdate
from utils import fetch_all_books, upload_books, fetch_one_book, update_books, del_book

router = APIRouter(prefix="/books")

@router.get("", status_code=200)
def get_books(session: Session = Depends(get_session)):
    return fetch_all_books(session)

@router.post("", status_code=201)
def post_books(books_info: BookData, session: Session = Depends(get_session)):
    return upload_books(books_info, session)

@router.get("/{book_id}", status_code=200)
def get_book(book_id: int, session: SessionDep):
    return fetch_one_book(book_id, session)

@router.patch("/{book_id}", status_code=200)
def patch_book(book_id: int, book_detail: BookUpdate, session: SessionDep):
    return update_books(book_id, book_detail, session)

@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, session: SessionDep):
   del_book(book_id, session)