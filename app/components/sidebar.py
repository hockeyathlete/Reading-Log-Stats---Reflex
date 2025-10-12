import reflex as rx


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
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
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
        class_name="w-64 bg-white h-full hidden lg:flex flex-col justify-between border-r border-gray-200 shadow-[1px_0_3px_rgba(0,0,0,0.02)]",
    )