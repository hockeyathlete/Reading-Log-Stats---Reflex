import reflex as rx
from sqlmodel import create_engine

engine = create_engine("sqlite:///reading_tracker.db")


def create_db_and_tables():
    from app.models import SQLModel

    SQLModel.metadata.create_all(engine)