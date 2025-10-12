import reflex as rx
from app.state import ReadingState
import datetime


def dialog_base(
    title: str, content: rx.Component, open_var: rx.Var, on_close: rx.event.EventHandler
) -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.el.div(
                rx.el.h3(title, class_name="text-xl font-semibold text-gray-800"),
                rx.dialog.close(
                    rx.el.button(
                        rx.icon("x", size=20, class_name="text-gray-500"),
                        class_name="p-1 rounded-full hover:bg-gray-100",
                    )
                ),
                class_name="flex justify-between items-center pb-4 border-b border-gray-200",
            ),
            content,
            style={
                "background_color": "white",
                "border_radius": "1rem",
                "padding": "2rem",
                "box_shadow": "0 25px 50px -12px rgba(0, 0, 0, 0.25)",
                "width": "100%",
                "max_width": "28rem",
                "margin": "1rem",
                "border": "1px solid #e5e7eb",
            },
        ),
        open=open_var,
        on_open_change=on_close,
    )


def add_book_form() -> rx.Component:
    return rx.el.form(
        rx.el.div(
            rx.el.label(
                "Title", class_name="text-sm font-medium text-gray-700 mb-1 block"
            ),
            rx.el.input(
                name="title",
                placeholder="The Hobbit",
                class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-1 focus:ring-teal-500 focus:border-teal-500",
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.label(
                "Author", class_name="text-sm font-medium text-gray-700 mb-1 block"
            ),
            rx.el.input(
                name="author",
                placeholder="J.R.R. Tolkien",
                class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-1 focus:ring-teal-500 focus:border-teal-500",
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.label(
                "Genre", class_name="text-sm font-medium text-gray-700 mb-1 block"
            ),
            rx.el.input(
                name="genre",
                placeholder="Fantasy",
                class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-1 focus:ring-teal-500 focus:border-teal-500",
            ),
            class_name="mb-6",
        ),
        rx.el.div(
            rx.el.button(
                "Cancel",
                type="button",
                on_click=ReadingState.toggle_add_book_dialog,
                class_name="w-full justify-center bg-gray-100 text-gray-700 px-4 py-2 rounded-lg font-semibold hover:bg-gray-200 transition-colors",
            ),
            rx.el.button(
                "Add Book",
                type="submit",
                class_name="w-full justify-center bg-teal-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-teal-700 transition-colors",
            ),
            class_name="flex gap-4 mt-4",
        ),
        on_submit=ReadingState.add_book,
        reset_on_submit=True,
        class_name="pt-6",
    )


def log_session_form() -> rx.Component:
    return rx.el.form(
        rx.el.div(
            rx.el.label(
                "Book", class_name="text-sm font-medium text-gray-700 mb-1 block"
            ),
            rx.el.select(
                rx.foreach(
                    ReadingState.books,
                    lambda book: rx.el.option(book.title, value=book.id.to_string()),
                ),
                name="book_id",
                class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-1 focus:ring-teal-500 focus:border-teal-500",
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.label(
                "Pages Read", class_name="text-sm font-medium text-gray-700 mb-1 block"
            ),
            rx.el.input(
                type="number",
                name="pages_read",
                placeholder="50",
                class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-1 focus:ring-teal-500 focus:border-teal-500",
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.label(
                "Date", class_name="text-sm font-medium text-gray-700 mb-1 block"
            ),
            rx.el.input(
                type="date",
                name="date",
                default_value=datetime.date.today().isoformat(),
                class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-1 focus:ring-teal-500 focus:border-teal-500",
            ),
            class_name="mb-6",
        ),
        rx.el.div(
            rx.el.button(
                "Cancel",
                type="button",
                on_click=ReadingState.toggle_log_session_dialog,
                class_name="w-full justify-center bg-gray-100 text-gray-700 px-4 py-2 rounded-lg font-semibold hover:bg-gray-200 transition-colors",
            ),
            rx.el.button(
                "Log Session",
                type="submit",
                class_name="w-full justify-center bg-teal-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-teal-700 transition-colors",
            ),
            class_name="flex gap-4 mt-4",
        ),
        on_submit=ReadingState.log_session,
        reset_on_submit=True,
        class_name="pt-6",
    )