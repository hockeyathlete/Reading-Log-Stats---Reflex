import reflex as rx
from dotenv import load_dotenv
from sqlmodel import create_engine
import os # Import the os module

# Retrieve the DATABASE_URL from environment variables
# Provide a default value for local development if not set, or raise an error if critical
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    from app.models import SQLModel
    SQLModel.metadata.create_all(engine)
