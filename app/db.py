from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

db_name = "library_circulation"
db_url = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@127.0.0.1:5432/{db_name}"

# connect_args = {
#     "check_same_thread": False
# }

engine = create_engine(db_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
def get_session():
    with Session(engine) as session:
        yield session