import reflex as rx
from sqlmodel import Field, SQLModel
import datetime
from typing import Optional


class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    author: str
    genre: str
    status: str
    rating: Optional[int] = Field(default=None)
    cover_url: str
    finished_date: Optional[datetime.date] = Field(default=None)


class ReadingLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: datetime.date
    book_id: int = Field(foreign_key="book.id")
    pages_read: int