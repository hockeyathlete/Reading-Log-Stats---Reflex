import reflex as rx
from app.state import ReadingState


def stat_card(icon: str, title: str, value: rx.Var, unit: str = "") -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, size=24, class_name="text-teal-600"),
            class_name="p-3 bg-teal-100 rounded-full",
        ),
        rx.el.div(
            rx.el.p(title, class_name="text-sm font-medium text-gray-500"),
            rx.el.div(
                rx.el.span(value, class_name="text-3xl font-bold text-gray-800"),
                rx.el.span(unit, class_name="text-base font-medium text-gray-600 ml-1"),
                class_name="flex items-baseline",
            ),
            class_name="mt-2",
        ),
        class_name="bg-white p-6 rounded-2xl border border-gray-200 flex flex-col justify-start shadow-[0_1px_3px_rgba(0,0,0,0.03)] hover:shadow-md hover:-translate-y-1 transition-all duration-300",
    )


def stats_grid() -> rx.Component:
    return rx.el.div(
        stat_card("book-up", "Reading Streak", ReadingState.reading_streak, "days"),
        stat_card("bar-chart-3", "Avg Pages/Day", ReadingState.avg_pages_per_day),
        stat_card("book-marked", "Books Finished", ReadingState.total_books_finished),
        stat_card("file-text", "Total Pages Read", ReadingState.total_pages_read),
        class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6",
    )