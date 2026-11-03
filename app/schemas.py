from sqlmodel import SQLModel, Field

class BookData(SQLModel):
    title: str = Field(min_length=3, max_length=120, description="Title must be 3-120 characters long")
    author: str = Field(min_length=2, max_length=80, description="Author Name must be 2-80 characters long")
    category: str = Field(description="Enter book category, cannot be empty")
    total_copies: int = Field(ge=1)
    available_copies: int = Field(ge=1)
    
class BookUpdate(SQLModel):
    title: str | None = Field(default=None, min_length=3, max_length=120, description="Title must be 3-120 characters long")
    author: str | None= Field(default=None, min_length=2, max_length=80, description="Author Name must be 2-80 characters long")
    category: str | None= Field(default=None, description="Enter book category, cannot be empty")
    
class BookTable(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(min_length=3, max_length=120, description="Title must be 3-120 characters long")
    author: str = Field(min_length=2, max_length=80, description="Author Name must be 2-80 characters long")
    category: str = Field(description="Enter book category, cannot be empty")
    total_copies: int = Field(ge=1)
    available_copies: int = Field(ge=1)
    
class Loan(SQLModel):
    book_id: int = Field(description="Id referencing the Book")
    borrower_name: str = Field(min_length=2, max_length=80, description="Borrower name with length between 2-80 characters")
    is_returned: bool = False
    
class LoanTable(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    book_id: int = Field(description="Id referencing the Book")
    borrower_name: str = Field(min_length=2, max_length=80, description="Borrower name with length between 2-80 characters")
    is_returned: bool = False