import reflex as rx
from app.state import ReadingState

TOOLTIP_PROPS = {
    "content_style": {
        "background": "white",
        "border_color": "#e5e7eb",
        "border_radius": "0.75rem",
        "box_shadow": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
        "font_family": "Raleway, sans-serif",
        "font_size": "14px",
    },
    "label_style": {"color": "#1f2937", "font_weight": "600"},
    "item_style": {"color": "#4b5563"},
    "separator": ": ",
}


def pages_per_day_chart() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Pages Read Per Day",
            class_name="text-lg font-semibold text-gray-800 mb-4 px-6",
        ),
        rx.recharts.area_chart(
            rx.recharts.cartesian_grid(
                horizontal=True, vertical=False, class_name="stroke-gray-200 opacity-50"
            ),
            rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
            rx.recharts.x_axis(
                data_key="date",
                tick_line=False,
                axis_line=False,
                tick_margin=10,
                data_type="category",
                allow_duplicated_category=False,
            ),
            rx.recharts.y_axis(
                allow_decimals=False, tick_line=False, axis_line=False, tick_margin=10
            ),
            rx.recharts.area(
                data_key="pages",
                type_="monotone",
                stroke="#009688",
                fill="rgba(0, 150, 136, 0.2)",
                stroke_width=2,
            ),
            data=ReadingState.pages_per_day_data,
            height=300,
            margin={"top": 10, "right": 30, "left": 0, "bottom": 0},
            class_name="font-sans",
        ),
        class_name="bg-white p-6 rounded-2xl border border-gray-200 shadow-[0_1px_3px_rgba(0,0,0,0.03)]",
    )


def books_per_month_chart() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Books Finished Per Month",
            class_name="text-lg font-semibold text-gray-800 mb-4 px-6",
        ),
        rx.recharts.bar_chart(
            rx.recharts.cartesian_grid(
                horizontal=False,
                vertical=False,
                class_name="stroke-gray-200 opacity-50",
            ),
            rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
            rx.recharts.x_axis(
                data_key="month", tick_line=False, axis_line=False, tick_margin=10
            ),
            rx.recharts.y_axis(
                allow_decimals=False,
                tick_line=False,
                axis_line=False,
                tick_margin=10,
                width=20,
            ),
            rx.recharts.bar(
                data_key="books", fill="#009688", radius=[4, 4, 0, 0], bar_size=20
            ),
            data=ReadingState.books_per_month_data,
            height=300,
            margin={"top": 10, "right": 30, "left": 0, "bottom": 0},
            class_name="font-sans",
        ),
        class_name="bg-white p-6 rounded-2xl border border-gray-200 shadow-[0_1px_3px_rgba(0,0,0,0.03)]",
    )