import reflex as rx
from app.models import Rubric
from app.states.rubric_state import RubricState
from app.states.project_state import ProjectState


def rubric_row(rubric: Rubric) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    rx.icon("file-code", class_name="w-5 h-5 text-[#0284c7]"),
                    class_name="w-10 h-10 rounded-full bg-[#0284c7]/10 flex items-center justify-center mr-3",
                ),
                rx.el.div(
                    rx.el.p(
                        rubric["name"], class_name="text-sm font-semibold text-gray-900"
                    ),
                    class_name="flex flex-col",
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.code(
                    rubric["kql_query"],
                    class_name="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs font-mono break-all line-clamp-2",
                ),
                rx.el.button(
                    rx.icon(
                        "copy", class_name="w-3 h-3 text-gray-400 hover:text-[#0284c7]"
                    ),
                    on_click=rx.set_clipboard(rubric["kql_query"]),
                    class_name="ml-2 p-1 hover:bg-gray-100 rounded transition-colors shrink-0",
                    title="Copy KQL",
                ),
                class_name="flex items-start justify-between gap-2",
            ),
            class_name="px-6 py-4 max-w-xs",
        ),
        rx.el.td(
            rx.el.div(
                rx.icon("folder", class_name="w-3 h-3 mr-1.5 text-gray-400"),
                rx.el.span(rubric["project_name"], class_name="text-sm text-gray-600"),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon("copy-plus", class_name="w-4 h-4"),
                    on_click=lambda: RubricState.duplicate_rubric(rubric),
                    class_name="p-1.5 text-purple-600 hover:bg-purple-50 rounded-md transition-colors",
                    title="Duplicate",
                ),
                rx.el.button(
                    rx.icon("pencil", class_name="w-4 h-4"),
                    on_click=lambda: RubricState.edit_rubric(rubric),
                    class_name="p-1.5 text-[#0284c7] hover:bg-[#0284c7]/10 rounded-md transition-colors",
                    title="Edit",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="w-4 h-4"),
                    on_click=lambda: RubricState.prompt_delete(rubric),
                    class_name="p-1.5 text-red-600 hover:bg-red-50 rounded-md transition-colors",
                    title="Delete",
                ),
                class_name="flex justify-end items-center gap-2",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        class_name="border-b border-gray-100 hover:bg-gray-50/80 transition-colors",
    )


def rubric_table() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "search",
                    class_name="w-5 h-5 text-gray-500 absolute left-4 top-1/2 -translate-y-1/2",
                ),
                rx.el.input(
                    placeholder="Search rubrics or KQL...",
                    on_change=RubricState.set_search_query.debounce(300),
                    class_name="pl-12 pr-6 py-3 w-full sm:w-80 rounded-full border border-gray-200 focus:ring-4 focus:ring-[#0284c7]/10 focus:border-[#0284c7] outline-none transition-all text-[15px] bg-white shadow-sm hover:shadow-md",
                ),
                class_name="relative",
            ),
            rx.el.div(
                rx.el.select(
                    rx.el.option("All Projects", value="All"),
                    rx.foreach(
                        ProjectState.projects,
                        lambda p: rx.el.option(p["name"], value=p["id"]),
                    ),
                    on_change=RubricState.set_filter_project_id,
                    class_name="pl-4 pr-10 py-3 rounded-full border border-gray-200 focus:ring-4 focus:ring-[#0284c7]/10 focus:border-[#0284c7] outline-none transition-all text-[15px] bg-white shadow-sm hover:shadow-md cursor-pointer",
                ),
                rx.el.button(
                    rx.icon("plus", class_name="w-5 h-5 mr-2.5"),
                    "New Rubric",
                    on_click=RubricState.toggle_add_dialog,
                    class_name="bg-[#0284c7] hover:bg-[#0270a9] text-white pl-5 pr-6 py-3 rounded-full text-[15px] font-bold shadow-[0_4px_14px_rgba(2,132,199,0.3)] hover:shadow-[0_6px_20px_rgba(2,132,199,0.4)] transition-all transform hover:-translate-y-0.5 active:translate-y-0 flex items-center",
                ),
                class_name="flex flex-col sm:flex-row gap-4",
            ),
            class_name="flex flex-col lg:flex-row justify-between items-center gap-4 mb-8",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Rubric Name",
                            class_name="px-8 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "KQL Query",
                            class_name="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Project",
                            class_name="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Actions",
                            class_name="px-8 py-4 text-right text-xs font-bold text-gray-500 uppercase tracking-wider",
                        ),
                        class_name="bg-gray-50/80 border-b border-gray-100",
                    )
                ),
                rx.el.tbody(
                    rx.foreach(RubricState.filtered_rubrics, rubric_row),
                    class_name="bg-white divide-y divide-gray-100",
                ),
                class_name="min-w-full divide-y divide-gray-100",
            ),
            class_name="overflow-x-auto rounded-[24px] border border-gray-100 shadow-[0_4px_24px_rgba(0,0,0,0.04)] bg-white",
        ),
        rx.el.div(
            rx.el.p(
                f"Showing {RubricState.filtered_rubrics.length()} rubrics",
                class_name="text-sm font-medium text-gray-500",
            ),
            class_name="mt-6 px-4",
        ),
        class_name="w-full",
    )