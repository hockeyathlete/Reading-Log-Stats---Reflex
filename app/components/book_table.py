import reflex as rx
from app.state import ReadingState
from app.models import Book
from app.components.forms import dialog_base


def rating_stars(rating: rx.Var[int | None]) -> rx.Component:
    """Displays a star rating component."""
    return rx.el.div(
        rx.cond(
            rating != None,
            rx.el.div(
                rx.foreach(
                    rx.Var.range(rating.to(int)),
                    lambda i: rx.icon(
                        "star", size=18, class_name="text-yellow-400 fill-yellow-400"
                    ),
                ),
                rx.foreach(
                    rx.Var.range(5 - rating.to(int)),
                    lambda i: rx.icon(
                        "star", size=18, class_name="text-gray-300 fill-gray-300"
                    ),
                ),
                class_name="flex items-center",
            ),
            rx.el.span("N/A", class_name="text-sm text-gray-500"),
        ),
        class_name="flex items-center",
    )


def book_row(book: Book, index: int) -> rx.Component:
    """A row in the book table."""
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.div(book.title, class_name="text-sm font-medium text-gray-900"),
                rx.el.div(book.author, class_name="text-sm text-gray-500"),
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            book.genre, class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
        ),
        rx.el.td(
            rx.el.span(
                book.status,
                class_name=rx.match(
                    book.status,
                    (
                        "Finished",
                        "px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800",
                    ),
                    (
                        "Reading",
                        "px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-teal-100 text-teal-800",
                    ),
                    (
                        "To Read",
                        "px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800",
                    ),
                    "px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-100 text-gray-800",
                ),
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(rating_stars(book.rating), class_name="px-6 py-4 whitespace-nowrap"),
        rx.el.td(
            rx.cond(
                (book.status == "Reading") | (book.status == "To Read"),
                rx.el.button(
                    rx.icon("square_check", size=20),
                    on_click=lambda: ReadingState.mark_book_finished(book.id),
                    class_name="text-gray-400 hover:text-green-600 transition-colors",
                ),
                rx.fragment(),
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right text-sm font-medium",
        ),
        on_click=lambda: ReadingState.open_book_detail_dialog(book.id),
        class_name=rx.cond(index % 2 == 0, "bg-white", "bg-gray-50/50")
        + " hover:bg-teal-50/60 cursor-pointer transition-colors",
    )


def book_detail_dialog_content() -> rx.Component:
    """Content for the book detail dialog."""
    return rx.cond(
        ReadingState.selected_book,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        ReadingState.selected_book.author,
                        class_name="text-sm text-gray-500",
                    ),
                    rx.el.p(
                        ReadingState.selected_book.genre,
                        class_name="text-sm text-gray-400",
                    ),
                    class_name="flex gap-2 items-center",
                ),
                class_name="mb-6",
            ),
            rx.el.div(
                rx.el.label(
                    "Status", class_name="text-sm font-medium text-gray-700 mb-1 block"
                ),
                rx.el.select(
                    rx.foreach(
                        ["Finished", "Reading", "To Read"],
                        lambda status: rx.el.option(status, value=status),
                    ),
                    value=ReadingState.selected_book.status,
                    on_change=ReadingState.update_selected_book_status,
                    class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-1 focus:ring-teal-500 focus:border-teal-500",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Rating", class_name="text-sm font-medium text-gray-700 mb-1 block"
                ),
                rx.el.div(
                    rx.foreach(
                        rx.Var.range(1, 6),
                        lambda i: rx.el.button(
                            rx.icon(
                                "star",
                                size=24,
                                class_name=rx.cond(
                                    ReadingState.selected_book.rating >= i,
                                    "text-yellow-400 fill-yellow-400",
                                    "text-gray-300",
                                ),
                            ),
                            on_click=lambda: ReadingState.update_selected_book_rating(
                                i
                            ),
                            class_name="p-1 hover:scale-110 transition-transform",
                        ),
                    ),
                    class_name="flex items-center",
                ),
                class_name="mb-6",
            ),
            rx.el.div(
                rx.el.button(
                    "Close",
                    on_click=ReadingState.close_book_detail_dialog,
                    class_name="w-full justify-center bg-teal-600 text-white px-4 py-2 rounded-lg font-semibold hover:bg-teal-700 transition-colors",
                ),
                class_name="flex justify-end mt-4",
            ),
            class_name="pt-6",
        ),
        rx.el.div("Loading..."),
    )


def book_table() -> rx.Component:
    """The main table component for displaying books."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.button(
                    rx.icon("menu", size=24),
                    on_click=ReadingState.toggle_mobile_sidebar,
                    class_name="lg:hidden p-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors",
                ),
                rx.el.h2(
                    "My Library",
                    class_name="text-2xl md:text-3xl font-bold text-gray-800",
                ),
                class_name="flex items-center gap-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "search",
                        class_name="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400",
                    ),
                    rx.el.input(
                        placeholder="Search...",
                        on_change=ReadingState.set_search_query.debounce(300),
                        class_name="w-full max-w-xs pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-1 focus:ring-teal-500 focus:border-teal-500 text-sm",
                    ),
                    class_name="relative flex-1",
                ),
                rx.el.button(
                    rx.icon("book-plus", size=16, class_name="mr-2"),
                    "Add Book",
                    on_click=ReadingState.toggle_add_book_dialog,
                    class_name="flex items-center bg-teal-600 text-white px-4 py-2 rounded-lg hover:bg-teal-700 font-semibold transition-all shadow-md hover:shadow-lg",
                ),
                class_name="flex items-center gap-2 md:gap-4",
            ),
            class_name="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "Title & Author",
                                scope="col",
                                class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Genre",
                                scope="col",
                                class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Status",
                                scope="col",
                                class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Rating",
                                scope="col",
                                class_name="px-6 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                            ),
                            rx.el.th(
                                "Actions",
                                scope="col",
                                class_name="px-6 py-3 text-right text-xs font-bold text-gray-500 uppercase tracking-wider",
                            ),
                        )
                    ),
                    rx.el.tbody(
                        rx.foreach(ReadingState.filtered_books, book_row),
                        class_name="bg-white divide-y divide-gray-200",
                    ),
                    class_name="min-w-full divide-y divide-gray-200",
                ),
                class_name="shadow-sm border-b border-gray-200 rounded-lg",
            ),
            class_name="overflow-x-auto",
        ),
        dialog_base(
            rx.cond(
                ReadingState.selected_book,
                ReadingState.selected_book.title,
                "Book Details",
            ),
            book_detail_dialog_content(),
            ReadingState.show_book_detail_dialog,
            ReadingState.close_book_detail_dialog,
        ),
        class_name="w-full",
    )