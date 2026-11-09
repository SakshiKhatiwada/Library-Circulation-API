from sqlmodel import SQLModel, create_engine, Session
from fastapi import Depends
from typing import Annotated
# import os
# from dotenv import load_dotenv
from config import settings

# load_dotenv()

# DB_USER = os.getenv("DB_USER")
# DB_PASSWORD = os.getenv("DB_PASSWORD")

# db_name = "library_circulation"
# db_url = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@127.0.0.1:5432/{db_name}"

if settings.db_url.startswith("sqlite"):
    connect_args = {
        "check_same_thread": False
    }
    engine = create_engine(settings.db_url, connect_args=connect_args)
else:
    engine = create_engine(settings.db_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
def get_session():
    with Session(engine) as session:
        yield session
        
SessionDep = Annotated[Session, Depends(get_session)]