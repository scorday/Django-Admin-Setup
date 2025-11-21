import reflex as rx
from app.components.sidebar import sidebar
from app.components.rubric_table import rubric_table
from app.components.rubric_dialogs import (
    add_rubric_dialog,
    edit_rubric_dialog,
    delete_rubric_dialog,
)
from app.states.rubric_state import RubricState


def stat_card(title: str, value: rx.Var, icon: str, color: str) -> rx.Component:
    colors = {
        "sky": ("text-sky-600", "bg-sky-50"),
        "green": ("text-green-600", "bg-green-50"),
        "blue": ("text-blue-600", "bg-blue-50"),
        "purple": ("text-purple-600", "bg-purple-50"),
        "orange": ("text-orange-600", "bg-orange-50"),
    }
    icon_color, bg_color = colors.get(color, ("text-gray-600", "bg-gray-50"))
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name=f"w-7 h-7 {icon_color}"),
            class_name=f"p-4 {bg_color} rounded-2xl w-fit mb-5 transition-transform group-hover:scale-110 duration-300 ease-out",
        ),
        rx.el.h3(
            title,
            class_name="text-gray-500 text-sm font-semibold tracking-wide uppercase",
        ),
        rx.el.p(
            value,
            class_name="text-3xl font-black text-gray-900 mt-2 font-['Lato'] tracking-tight",
        ),
        class_name="bg-white p-7 rounded-[24px] border border-gray-100/50 shadow-[0_2px_8px_rgba(0,0,0,0.04)] hover:shadow-[0_8px_24px_rgba(0,0,0,0.08)] transition-all duration-300 ease-[cubic-bezier(0.4,0,0.2,1)] group hover:-translate-y-1",
    )


def rubrics_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1(
                    "Rubric Management",
                    class_name="text-4xl font-black text-gray-900 mb-2 font-['Lato'] tracking-tight",
                ),
                rx.el.p(
                    "Manage KQL query rubrics for projects.",
                    class_name="text-lg text-gray-500 mb-10 font-medium",
                ),
                rx.el.div(
                    stat_card(
                        "Total Rubrics",
                        RubricState.total_rubrics.to_string(),
                        "file-code",
                        "purple",
                    ),
                    stat_card(
                        "Projects Covered",
                        RubricState.unique_projects_count.to_string(),
                        "folder-check",
                        "sky",
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-12",
                ),
                rubric_table(),
                add_rubric_dialog(),
                edit_rubric_dialog(),
                delete_rubric_dialog(),
                class_name="max-w-screen-2xl mx-auto",
            ),
            class_name="lg:ml-[280px] p-8 lg:p-12 min-h-screen bg-[#f8f9fa]",
        ),
        class_name="font-['Lato'] text-gray-900 bg-[#f8f9fa] min-h-screen",
    )