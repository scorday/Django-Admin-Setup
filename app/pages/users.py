import reflex as rx
from app.components.sidebar import sidebar
from app.components.user_table import user_table
from app.components.user_dialogs import (
    add_user_dialog,
    edit_user_dialog,
    delete_user_dialog,
)


def users_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1(
                    "User Management",
                    class_name="text-4xl font-black text-gray-900 mb-2 font-['Lato'] tracking-tight",
                ),
                rx.el.p(
                    "Manage system access and user roles.",
                    class_name="text-lg text-gray-500 mb-10 font-medium",
                ),
                user_table(),
                add_user_dialog(),
                edit_user_dialog(),
                delete_user_dialog(),
                class_name="max-w-screen-2xl mx-auto",
            ),
            class_name="lg:ml-[280px] p-8 lg:p-12 min-h-screen bg-[#f8f9fa]",
        ),
        class_name="font-['Lato'] text-gray-900 bg-[#f8f9fa] min-h-screen",
    )