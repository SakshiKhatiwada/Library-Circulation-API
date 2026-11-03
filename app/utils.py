from sqlmodel import Session, select

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