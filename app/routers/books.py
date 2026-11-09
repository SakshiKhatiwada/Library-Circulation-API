from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select, or_
from typing import Annotated

from db import get_session, SessionDep
from schemas import BookData, BookUpdate, BookFilter, BookTable
from utils.books import fetch_all_books, upload_books, fetch_one_book, update_books, del_book

router = APIRouter(prefix="/books", tags=["books"])

@router.get("", status_code=200)
def get_books(filter: Annotated[BookFilter | None, Query()] = None, session: Session = Depends(get_session)):
    if filter is None:
        return fetch_all_books(session)

    statement = select(BookTable)
    # incremental filter statement banaayera last maa ek choti execute garnu parxa
    
    if filter.search:
        search_term = f"%{filter.search}%"
        statement = statement.where(
            or_(
                BookTable.title.ilike(search_term),
                BookTable.author.ilike(search_term)
            )
        )
    if filter.category:
        statement = statement.where(filter.category== BookTable.category)
        
    if filter.available_only:
        statement = statement.where(BookTable.available_copies >= 1)
    
    return session.exec(statement).all()
    
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