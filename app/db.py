import reflex as rx
from sqlmodel import create_engine
import os # Import the os module

# Retrieve the DATABASE_URL from environment variables
# Provide a default value for local development if not set, or raise an error if critical
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres123@localhost:5432/reading_tracker_reflex")

engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    from app.models import SQLModel
    SQLModel.metadata.create_all(engine)
