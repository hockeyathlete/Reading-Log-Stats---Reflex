import reflex as rx
from app.state import ReadingState


def header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.h2("Dashboard", class_name="text-3xl font-bold text-gray-800"),
            rx.el.p(
                f"Welcome back! Here's your reading summary.",
                class_name="text-gray-500 mt-1",
            ),
            class_name="flex-1",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("plus", size=16, class_name="mr-2"),
                "Log Session",
                on_click=ReadingState.toggle_log_session_dialog,
                class_name="flex items-center bg-white text-gray-700 px-4 py-2 rounded-lg border border-gray-300 hover:bg-gray-50 font-semibold transition-all shadow-sm",
            ),
            rx.el.button(
                rx.icon("book-plus", size=16, class_name="mr-2"),
                "Add Book",
                on_click=ReadingState.toggle_add_book_dialog,
                class_name="flex items-center bg-teal-600 text-white px-4 py-2 rounded-lg hover:bg-teal-700 font-semibold transition-all shadow-md hover:shadow-lg",
            ),
            class_name="flex items-center gap-4",
        ),
        class_name="flex justify-between items-center w-full",
    )