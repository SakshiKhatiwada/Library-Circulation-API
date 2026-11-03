from sqlmodel import Session, select
from fastapi import HTTPException

from schemas import BookTable, BookData, BookUpdate

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
        book = result.one()
    except:
        raise HTTPException(status_code=404, detail="book not found")
    return book

def update_books(book_id: int, book_details: BookUpdate, session: Session):
    statement = select(BookTable).where(BookTable.id == book_id)
    result = session.exec(statement)
    try:
        book = result.one()
    except:
        raise HTTPException(status_code=404, detail="book not found")
    
    update_data = book_details.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(book, key, value)
    
    session.add(book)
    session.commit()
    session.refresh(book)
    
    return book

def del_book(book_id: int, session: Session):
    statement = select(BookTable).where(BookTable.id == book_id)
    try:
        result = session.exec(statement)
        try:
            book = result.one()
        except:
            raise HTTPException(status_code=404, detail="book not found")
    except HTTPException:
        raise
    except:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    session.delete(book)
    session.commit()