import reflex as rx
from app.components.sidebar import sidebar
from app.components.header import header
from app.components.stats import stats_grid
from app.components.charts import pages_per_day_chart, books_per_month_chart
from app.components.forms import dialog_base, add_book_form, log_session_form
from app.state import ReadingState
from app.components.book_table import book_table
from app.components.reading_log_table import reading_log_table
from app.db import create_db_and_tables


def dashboard() -> rx.Component:
    return rx.el.main(
        header(),
        rx.el.div(stats_grid(), class_name="mt-8"),
        rx.el.div(
            pages_per_day_chart(),
            books_per_month_chart(),
            class_name="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-6",
        ),
        class_name="flex-1 p-8 overflow-y-auto",
    )


def index() -> rx.Component:
    return rx.el.div(
        sidebar(),
        dashboard(),
        dialog_base(
            "Add a New Book",
            add_book_form(),
            ReadingState.show_add_book_dialog,
            ReadingState.toggle_add_book_dialog,
        ),
        dialog_base(
            "Log a Reading Session",
            log_session_form(),
            ReadingState.show_log_session_dialog,
            ReadingState.toggle_log_session_dialog,
        ),
        class_name="flex bg-gray-50 font-['Raleway'] min-h-screen",
    )


def library() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(book_table(), class_name="flex-1 p-8 overflow-y-auto"),
        class_name="flex bg-gray-50 font-['Raleway'] min-h-screen",
    )


def log() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(reading_log_table(), class_name="flex-1 p-8 overflow-y-auto"),
        class_name="flex bg-gray-50 font-['Raleway'] min-h-screen",
    )


app = rx.App(
    theme=rx.theme(appearance="light", accent_color="teal"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Raleway:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/", on_load=ReadingState.on_load)
app.add_page(library, route="/library", on_load=ReadingState.on_load)
app.add_page(log, route="/log", on_load=ReadingState.on_load)
create_db_and_tables()