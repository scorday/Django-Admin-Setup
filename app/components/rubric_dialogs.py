import reflex as rx
from app.states.rubric_state import RubricState
from app.states.project_state import ProjectState


def form_input(
    label: str, placeholder: str, value: rx.Var, on_change: rx.event.EventHandler
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-gray-700 mb-1"),
        rx.el.input(
            placeholder=placeholder,
            default_value=value,
            on_change=on_change,
            class_name="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#0284c7] focus:border-transparent outline-none transition-all text-sm",
        ),
        class_name="mb-4",
    )


def form_textarea(
    label: str, placeholder: str, value: rx.Var, on_change: rx.event.EventHandler
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-gray-700 mb-1"),
        rx.el.textarea(
            placeholder=placeholder,
            default_value=value,
            on_change=on_change,
            class_name="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#0284c7] focus:border-transparent outline-none transition-all text-sm h-32 font-mono bg-gray-50 resize-none",
        ),
        class_name="mb-4",
    )


def project_select(value: rx.Var, on_change: rx.event.EventHandler) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            "Assigned Project",
            class_name="block text-sm font-medium text-gray-700 mb-1",
        ),
        rx.el.select(
            rx.el.option("Select a project", value="", disabled=True),
            rx.foreach(
                ProjectState.projects, lambda p: rx.el.option(p["name"], value=p["id"])
            ),
            value=value,
            on_change=on_change,
            class_name="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-[#0284c7] focus:border-transparent outline-none transition-all text-sm bg-white",
        ),
        class_name="mb-6",
    )


def add_rubric_dialog() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-gray-900/40 backdrop-blur-[2px] z-50 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0"
            ),
            rx.radix.primitives.dialog.content(
                rx.radix.primitives.dialog.title(
                    "New Rubric",
                    class_name="text-2xl font-bold text-gray-900 mb-2 font-['Lato'] tracking-tight",
                ),
                rx.radix.primitives.dialog.description(
                    "Create a new KQL rubric for a project.",
                    class_name="text-[15px] text-gray-500 mb-8",
                ),
                project_select(
                    RubricState.form_project_id, RubricState.set_form_project_id
                ),
                form_input(
                    "Rubric Name",
                    "e.g. High Error Rate",
                    RubricState.form_name,
                    RubricState.set_form_name,
                ),
                form_textarea(
                    "KQL Query",
                    "e.g. error_code >= 500",
                    RubricState.form_kql_query,
                    RubricState.set_form_kql_query,
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancel",
                        on_click=RubricState.toggle_add_dialog,
                        class_name="px-6 py-2.5 text-sm font-bold text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-full transition-all mr-2",
                    ),
                    rx.el.button(
                        "Create Rubric",
                        on_click=RubricState.save_new_rubric,
                        class_name="px-6 py-2.5 text-sm font-bold text-white bg-[#0284c7] hover:bg-[#0270a9] rounded-full shadow-lg hover:shadow-xl transition-all transform hover:-translate-y-0.5",
                    ),
                    class_name="flex justify-end mt-8",
                ),
                class_name="fixed top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%] z-50 w-full max-w-lg bg-white rounded-[28px] p-8 shadow-[0_25px_50px_-12px_rgba(0,0,0,0.25)] outline-none focus:outline-none data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%] data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%] border border-gray-100",
            ),
        ),
        open=RubricState.is_add_open,
        on_open_change=RubricState.toggle_add_dialog,
    )


def edit_rubric_dialog() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/40 backdrop-blur-sm z-50"
            ),
            rx.radix.primitives.dialog.content(
                rx.radix.primitives.dialog.title(
                    "Edit Rubric",
                    class_name="text-xl font-bold text-gray-900 mb-4 font-['Lato']",
                ),
                project_select(
                    RubricState.form_project_id, RubricState.set_form_project_id
                ),
                form_input(
                    "Rubric Name",
                    "Rubric Name",
                    RubricState.form_name,
                    RubricState.set_form_name,
                ),
                form_textarea(
                    "KQL Query",
                    "KQL Query",
                    RubricState.form_kql_query,
                    RubricState.set_form_kql_query,
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancel",
                        on_click=RubricState.cancel_edit,
                        class_name="px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-lg transition-colors mr-2",
                    ),
                    rx.el.button(
                        "Save Changes",
                        on_click=RubricState.save_edited_rubric,
                        class_name="px-4 py-2 text-sm font-medium text-white bg-[#0284c7] hover:bg-[#026aa1] rounded-lg shadow-md hover:shadow-lg transition-all",
                    ),
                    class_name="flex justify-end mt-6",
                ),
                class_name="fixed top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%] z-50 w-full max-w-md bg-white rounded-2xl p-6 shadow-2xl outline-none",
            ),
        ),
        open=RubricState.is_edit_open,
        on_open_change=RubricState.cancel_edit,
    )


def delete_rubric_dialog() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/40 backdrop-blur-sm z-50"
            ),
            rx.radix.primitives.dialog.content(
                rx.radix.primitives.dialog.title(
                    "Delete Rubric?",
                    class_name="text-xl font-bold text-gray-900 mb-2 font-['Lato']",
                ),
                rx.el.p(
                    f"Are you sure you want to delete '{RubricState.form_name}'? This action cannot be undone.",
                    class_name="text-gray-600 mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancel",
                        on_click=RubricState.cancel_delete,
                        class_name="px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-lg transition-colors mr-2",
                    ),
                    rx.el.button(
                        "Delete Rubric",
                        on_click=RubricState.confirm_delete,
                        class_name="px-4 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-lg shadow-md hover:shadow-lg transition-all",
                    ),
                    class_name="flex justify-end",
                ),
                class_name="fixed top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%] z-50 w-full max-w-md bg-white rounded-2xl p-6 shadow-2xl outline-none",
            ),
        ),
        open=RubricState.is_delete_open,
        on_open_change=RubricState.cancel_delete,
    )