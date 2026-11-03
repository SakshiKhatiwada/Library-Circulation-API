from sqlmodel import Session, select
from fastapi import HTTPException

from schemas import Loan, LoanTable, LoanUpdate
from utils.books import does_book_exist, update_book_available_copies

def create_loan(loan_info: Loan, session: Session):
    if does_book_exist(loan_info.book_id, session):
        loan = LoanTable.model_validate(loan_info)
        returned_book = update_book_available_copies(loan_info.book_id, session, increment=False)
    
        session.add(loan)
        session.add(returned_book)
        session.commit()
        session.refresh(loan)
        session.refresh(returned_book)
        
        
    else:
        raise HTTPException(status_code=404, detail="loan can't be created, book does not exist")
    
    return loan

def fetch_loan(session: Session, active_only: bool = False):
    try:
        if active_only:
            statement = select(LoanTable).where(LoanTable.is_returned == False)
        else:
            statement = select(LoanTable)
            
        results = session.exec(statement)
        loan_details = results.all()
        
        return loan_details
    except:
        raise HTTPException(status_code=500, detail="Internal Server Error")

def fetch_loan_with_id(loan_id: int, session: Session):
    try:
        loans = session.exec(select(LoanTable).where(LoanTable.id == loan_id)).one()
        return loans     
    except:
        raise HTTPException(status_code=404, detail="Loan for the given id not found")
        
def mark_book_returned(loan_id: int, session: Session):
    loan: LoanTable = fetch_loan_with_id(loan_id, session)
    if loan.is_returned:
        raise HTTPException(status_code=409, detail="Conflict, book is already returned")
        
    loan.is_returned = True
    copies_available = update_book_available_copies(loan.book_id, session, increment=True)
    
    session.add(loan)
    session.add(copies_available)
    session.commit()
    session.refresh(loan)
    session.refresh(copies_available)
    
    return loan