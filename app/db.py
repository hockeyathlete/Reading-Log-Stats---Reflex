import reflex as rx
from sqlmodel import create_engine

engine = create_engine("postgresql+psycopg2://postgres:postgres123@localhost:5432/reading_tracker_reflex")


def create_db_and_tables():
    from app.models import SQLModel

    SQLModel.metadata.create_all(engine)