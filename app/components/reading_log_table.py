import reflex as rx
from app.state import ReadingState
from app.models import ReadingLog


def get_book_title_for_log(log: ReadingLog) -> rx.Component:
    return rx.foreach(
        ReadingState.books,
        lambda book: rx.cond(
            book.id == log.book_id,
            rx.el.div(
                rx.el.div(book.title, class_name="text-sm font-medium text-gray-900"),
                rx.el.div(book.author, class_name="text-sm text-gray-500"),
            ),
            rx.fragment(),
        ),
    )


def log_row(log: ReadingLog, index: int) -> rx.Component:
    """A row in the reading log table."""
    return rx.el.tr(
        rx.el.td(
            log.date.to_string(),
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-600",
        ),
        rx.el.td(get_book_title_for_log(log), class_name="px-6 py-4 whitespace-nowrap"),
        rx.el.td(
            rx.el.span(log.pages_read, class_name="font-medium text-gray-800"),
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-600",
        ),
        class_name=rx.cond(index % 2 == 0, "bg-white", "bg-gray-50/50 hover:bg-gray-50")
        + " transition-colors",
    )


def reading_log_table() -> rx.Component:
    """The main table component for displaying the reading log."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.button(
                    rx.icon("menu", size=24),
                    on_click=ReadingState.toggle_mobile_sidebar,
                    class_name="lg:hidden p-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors",
                ),
                rx.el.h2(
                    "Daily Reading Log",
                    class_name="text-2xl md:text-3xl font-bold text-gray-800",
                ),
                class_name="flex items-center gap-4",
            ),
            rx.el.div(
                rx.icon(
                    "search",
                    class_name="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400",
                ),
                rx.el.input(
                    placeholder="Search by book title...",
                    on_change=ReadingState.set_log_search_query.debounce(300),
                    class_name="w-full max-w-xs pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-1 focus:ring-teal-500 focus:border-teal-500 text-sm",
                ),
                class_name="relative",
            ),
            class_name="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "Date",
                                scope="col",
                                class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Book Title",
                                scope="col",
                                class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Pages Read",
                                scope="col",
                                class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                            ),
                        )
                    ),
                    rx.el.tbody(
                        rx.foreach(ReadingState.filtered_daily_log, log_row),
                        class_name="bg-white divide-y divide-gray-200",
                    ),
                    class_name="min-w-full divide-y divide-gray-200",
                ),
                class_name="shadow-sm border-b border-gray-200 rounded-lg",
            ),
            class_name="overflow-x-auto",
        ),
        class_name="w-full",
    )