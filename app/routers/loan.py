from fastapi import APIRouter, Query, HTTPException
from typing import Annotated

from db import SessionDep
from schemas import Loan, LoanTable
from sqlmodel import select
from utils.books import does_book_exist, update_book_available_copies
from utils.loan import create_loan
router = APIRouter(prefix="/loan", tags=["loan"])

@router.get("", status_code=200)
def get_loan(session: SessionDep, active_only: Annotated[bool, Query()] = False):
    if active_only:
        statement = select(LoanTable).where(LoanTable.is_returned == False)
    else:
        statement = select(LoanTable)
        
    results = session.exec(statement)
    loan_details = results.all()
    
    return loan_details

@router.post("", status_code=201)
def post_loan(loan_info: Loan, session: SessionDep):
    return create_loan(loan_info, session)