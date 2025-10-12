import reflex as rx
from app.state import ReadingState


def sidebar_link(text: str, icon: str, url: str) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.icon(
                icon,
                size=22,
                class_name="text-gray-500 group-hover:text-teal-600 transition-colors",
            ),
            rx.el.span(
                text,
                class_name="text-base font-medium text-gray-700 group-hover:text-teal-600 transition-colors",
            ),
            class_name="flex items-center gap-4 px-4 py-3 rounded-lg hover:bg-teal-50 transition-colors group",
        ),
        href=url,
        on_click=ReadingState.toggle_mobile_sidebar,
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.cond(
            ReadingState.show_mobile_sidebar,
            rx.el.button(
                rx.icon("x", size=24),
                on_click=ReadingState.toggle_mobile_sidebar,
                class_name="absolute top-4 right-4 p-2 text-gray-700 hover:bg-gray-100 rounded-lg lg:hidden z-50",
            ),
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("book-open", size=32, class_name="text-teal-600"),
                rx.el.h1(
                    "Bookworm",
                    class_name="text-2xl font-bold text-gray-800 tracking-tight",
                ),
                class_name="flex items-center gap-3 px-4 pt-6 pb-8",
            ),
            rx.el.nav(
                sidebar_link("Dashboard", "layout-dashboard", "/"),
                sidebar_link("My Library", "library", "/library"),
                sidebar_link("Reading Log", "list-checks", "/log"),
                class_name="flex flex-col gap-2 px-2",
            ),
        ),
        rx.el.div(
            sidebar_link("Settings", "settings", "/settings"),
            sidebar_link("Help", "life-buoy", "/help"),
            class_name="flex flex-col gap-2 px-2 pb-4",
        ),
        class_name=rx.cond(
            ReadingState.show_mobile_sidebar,
            "fixed top-0 left-0 h-full w-64 bg-white z-50 transform translate-x-0 transition-transform duration-300 ease-out flex flex-col justify-between border-r border-gray-200 shadow-[1px_0_3px_rgba(0,0,0,0.02)]",
            "fixed top-0 left-0 h-full w-64 bg-white z-50 transform -translate-x-full transition-transform duration-300 ease-out lg:relative lg:translate-x-0 lg:flex flex-col justify-between border-r border-gray-200 shadow-[1px_0_3px_rgba(0,0,0,0.02)]",
        ),
    )