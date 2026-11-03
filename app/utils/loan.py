from sqlmodel import Session, select
from fastapi import HTTPException

from schemas import Loan, LoanTable, LoanUpdate
from utils.books import does_book_exist, update_book_available_copies

def create_loan(loan_info: Loan, session: Session):
    if does_book_exist(loan_info.book_id, session):
        loan = LoanTable.model_validate(loan_info)
        returned_book = update_book_available_copies(loan_info.book_id, session)
    
        session.add(loan)
        session.add(returned_book)
        session.commit()
        session.refresh(loan)
        session.refresh(returned_book)
        
        
    else:
        raise HTTPException(status_code=404, detail="loan can't be created, book does not exist")
    
    return loan