from sqlmodel import Session, select
from fastapi import HTTPException

from schemas import BookTable, BookData, BookUpdate, LoanTable

def fetch_all_books(session: Session):
    statement = select(BookTable)
    results = session.exec(statement=statement)
    print(results)
    return results.all()

def upload_books(book_info: BookData, session: Session):
    try:
        new_book = BookTable(
            **book_info.model_dump(),
            available_copies = book_info.total_copies
        )
    except:
        raise HTTPException(status_code=422, detail="Validation Error")
    session.add(new_book)
    session.commit()
    session.refresh(new_book)
    
    return new_book

def fetch_one_book(book_id: int, session: Session) -> BookTable:
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
    book = session.get(BookTable, book_id)
    
    if not book:
        raise HTTPException(status_code=404, detail="book not found")
        
    loan_exists = session.exec(
        select(LoanTable.id)
        .where(LoanTable.book_id == book_id)
        .limit(1)
    ).first()
    
    if loan_exists:
        raise HTTPException(status_code=409, detail="Conflict. Can't Delete this book, it has loan history.")
    session.delete(book)
    session.commit()
    
def does_book_exist(book_id, session: Session):
    statement = select(BookTable).where(BookTable.id == book_id)
    result = session.exec(statement)
    try:  
        if result.one():
            return True
    except:
       return False

def book_available_copies(book_id: int, session: Session):
    book = fetch_one_book(book_id, session)
    return book.available_copies

def update_book_available_copies(book_id: int, session: Session, increment: bool = False):
    book = fetch_one_book(book_id, session)
    if book.available_copies < 0 or book.available_copies > book.total_copies:
        raise ValueError("Available copies cannot be less than 0 or greater than total copies")
        
    if book.available_copies == 0 and not increment:
        raise HTTPException(status_code=409, detail="Conflict, NO more copies available to loan")
        
    if increment:
        book.available_copies += 1
    else:
        book.available_copies -=1
        
    return book