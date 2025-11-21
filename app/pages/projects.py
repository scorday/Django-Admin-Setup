import reflex as rx
from app.components.sidebar import sidebar
from app.components.project_table import project_table
from app.components.project_dialogs import (
    add_project_dialog,
    edit_project_dialog,
    delete_project_dialog,
)


def projects_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1(
                    "Projects",
                    class_name="text-4xl font-black text-gray-900 mb-2 font-['Lato'] tracking-tight",
                ),
                rx.el.p(
                    "Manage development projects and track status.",
                    class_name="text-lg text-gray-500 mb-10 font-medium",
                ),
                project_table(),
                add_project_dialog(),
                edit_project_dialog(),
                delete_project_dialog(),
                class_name="max-w-screen-2xl mx-auto",
            ),
            class_name="lg:ml-[280px] p-8 lg:p-12 min-h-screen bg-[#f8f9fa]",
        ),
        class_name="font-['Lato'] text-gray-900 bg-[#f8f9fa] min-h-screen",
    )