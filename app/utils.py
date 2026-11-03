from sqlmodel import Session, select
from fastapi import HTTPException

from schemas import BookTable, BookData

def fetch_all_books(session: Session):
    statement = select(BookTable)
    results = session.exec(statement=statement)
    print(results)
    return results.all()

def upload_books(book_info : BookData, session: Session):
    books = BookTable.model_validate(book_info)
    
    session.add(books)
    session.commit()
    session.refresh(books)
    
    return books

def fetch_one_book(book_id: int, session: Session):
    statement = select(BookTable).where(BookTable.id == book_id)
    result = session.exec(statement)
    try:
        book = result.one_or_none()
    except:
        raise HTTPException(status_code=404, detail="book not found")
    return book