import reflex as rx
import datetime
from sqlmodel import select, Session
from app.db import engine
from app.models import Book, ReadingLog


class ReadingState(rx.State):
    books: list[Book] = []
    daily_log: list[ReadingLog] = []
    show_add_book_dialog: bool = False
    show_log_session_dialog: bool = False
    show_book_detail_dialog: bool = False
    selected_book_id: int | None = None
    search_query: str = ""
    log_search_query: str = ""
    show_mobile_sidebar: bool = False

    @rx.event
    def on_load(self):
        with Session(engine) as session:
            self.books = session.exec(select(Book)).all()
            self.daily_log = session.exec(select(ReadingLog)).all()

    @rx.var
    def filtered_books(self) -> list[Book]:
        """Filters books based on the search query."""
        if not self.search_query:
            return self.books
        query = self.search_query.lower()
        return [
            book
            for book in self.books
            if query in book.title.lower() or query in book.author.lower()
        ]

    @rx.var
    def filtered_daily_log(self) -> list[ReadingLog]:
        """Filters daily logs based on the log search query."""
        if not self.log_search_query:
            return self.daily_log
        query = self.log_search_query.lower()
        book_titles = {book.id: book.title.lower() for book in self.books}
        return [
            log
            for log in self.daily_log
            if log.book_id in book_titles and query in book_titles[log.book_id]
        ]

    @rx.var
    def selected_book(self) -> Book | None:
        if self.selected_book_id is None:
            return None
        for book in self.books:
            if book.id == self.selected_book_id:
                return book
        return None

    @rx.var
    def total_pages_read(self) -> int:
        return sum((log.pages_read for log in self.daily_log))

    @rx.var
    def total_books_finished(self) -> int:
        return len([book for book in self.books if book.status == "Finished"])

    @rx.var
    def reading_streak(self) -> int:
        if not self.daily_log:
            return 0
        dates = sorted(list(set((log.date for log in self.daily_log))))
        if not dates:
            return 0
        streak = 0
        max_streak = 0
        for i, date_obj in enumerate(dates):
            if i == 0:
                streak = 1
            else:
                prev_date_obj = dates[i - 1]
                if (date_obj - prev_date_obj).days == 1:
                    streak += 1
                elif (date_obj - prev_date_obj).days > 1:
                    max_streak = max(max_streak, streak)
                    streak = 1
        max_streak = max(max_streak, streak)
        today = datetime.date.today()
        if not dates or (today - dates[-1]).days > 1:
            return max_streak
        return streak

    @rx.var
    def avg_pages_per_day(self) -> float:
        if not self.daily_log:
            return 0.0
        num_days = len(set((log.date for log in self.daily_log)))
        return round(self.total_pages_read / num_days, 1) if num_days > 0 else 0.0

    @rx.var
    def pages_per_day_data(self) -> list[dict[str, int | str]]:
        pages_by_date = {}
        for log in self.daily_log:
            date_str = log.date.isoformat()
            pages_by_date[date_str] = pages_by_date.get(date_str, 0) + log.pages_read
        sorted_dates = sorted(pages_by_date.keys())
        return [{"date": date, "pages": pages_by_date[date]} for date in sorted_dates]

    @rx.var
    def books_per_month_data(self) -> list[dict[str, int | str]]:
        books_by_month = {}
        finished_books = [
            book
            for book in self.books
            if book.status == "Finished" and book.finished_date
        ]
        if not finished_books:
            min_year = datetime.date.today().year
        else:
            min_year = min((book.finished_date.year for book in finished_books))
        current_year = datetime.date.today().year
        for year in range(min_year, current_year + 1):
            for book in finished_books:
                if book.finished_date.year == year:
                    month_name = book.finished_date.strftime("%b %y")
                    books_by_month[month_name] = books_by_month.get(month_name, 0) + 1
        all_months_in_range = []
        for year in range(min_year, current_year + 1):
            for month_num in range(1, 13):
                if year == current_year and month_num > datetime.date.today().month:
                    break
                all_months_in_range.append(
                    datetime.date(year, month_num, 1).strftime("%b %y")
                )
        return [
            {"month": month, "books": books_by_month.get(month, 0)}
            for month in all_months_in_range
        ]

    @rx.event
    def toggle_add_book_dialog(self):
        self.show_add_book_dialog = not self.show_add_book_dialog

    @rx.event
    def toggle_log_session_dialog(self):
        self.show_log_session_dialog = not self.show_log_session_dialog

    @rx.event
    def toggle_mobile_sidebar(self):
        self.show_mobile_sidebar = not self.show_mobile_sidebar

    @rx.event
    def add_book(self, form_data: dict):
        with Session(engine) as session:
            new_book = Book(
                title=form_data.get("title", "Untitled"),
                author=form_data.get("author", "Unknown Author"),
                genre=form_data.get("genre", "Uncategorized"),
                status="To Read",
                cover_url="/placeholder.svg",
            )
            session.add(new_book)
            session.commit()
            session.refresh(new_book)
            self.books.append(new_book)
        self.show_add_book_dialog = False

    @rx.event
    def log_session(self, form_data: dict):
        with Session(engine) as session:
            new_log = ReadingLog(
                date=datetime.date.fromisoformat(form_data.get("date")),
                book_id=int(form_data.get("book_id")),
                pages_read=int(form_data.get("pages_read")),
            )
            session.add(new_log)
            session.commit()
            session.refresh(new_log)
            self.daily_log.append(new_log)
        self.show_log_session_dialog = False
        return ReadingState.on_load()

    @rx.event
    def mark_book_finished(self, book_id: int):
        with Session(engine) as session:
            book = session.get(Book, book_id)
            if book:
                book.status = "Finished"
                book.finished_date = datetime.date.today()
                session.add(book)
                session.commit()
                session.refresh(book)
                return ReadingState.on_load()

    @rx.event
    def open_book_detail_dialog(self, book_id: int):
        self.selected_book_id = book_id
        self.show_book_detail_dialog = True

    @rx.event
    def close_book_detail_dialog(self):
        self.show_book_detail_dialog = False
        self.selected_book_id = None

    @rx.event
    def update_selected_book_status(self, status: str):
        if self.selected_book_id is None:
            return
        with Session(engine) as session:
            book = session.get(Book, self.selected_book_id)
            if book:
                book.status = status
                if status == "Finished" and book.finished_date is None:
                    book.finished_date = datetime.date.today()
                elif status != "Finished":
                    book.finished_date = None
                session.add(book)
                session.commit()
                session.refresh(book)
                return ReadingState.on_load()

    @rx.event
    def update_selected_book_rating(self, rating: int):
        if self.selected_book_id is None:
            return
        with Session(engine) as session:
            book = session.get(Book, self.selected_book_id)
            if book:
                book.rating = None if book.rating == rating else rating
                session.add(book)
                session.commit()
                session.refresh(book)
                return ReadingState.on_load()