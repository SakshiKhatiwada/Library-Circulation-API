from fastapi import APIRouter, Query, HTTPException
from typing import Annotated

from db import SessionDep
from schemas import Loan, LoanTable
from sqlmodel import select
from utils.loan import create_loan, fetch_loan, mark_book_returned
router = APIRouter(prefix="/loans", tags=["loan"])

@router.get("", status_code=200)
def get_loan(session: SessionDep, active_only: Annotated[bool, Query()] = False):
    return fetch_loan(session, active_only=active_only)

@router.post("", status_code=201)
def post_loan(loan_info: Loan, session: SessionDep):
    return create_loan(loan_info, session)

@router.patch("/{loan_id}/return", status_code=200)
def update_return(loan_id: int, session: SessionDep):
    return mark_book_returned(loan_id, session)