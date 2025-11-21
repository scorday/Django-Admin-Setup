import reflex as rx
from app.models import Project
from app.states.project_state import ProjectState


def status_badge(status: str) -> rx.Component:
    return rx.el.span(
        status,
        class_name=rx.match(
            status,
            (
                "Active",
                "bg-green-50 text-green-700 border border-green-200 px-2.5 py-0.5 rounded-full text-xs font-medium",
            ),
            (
                "Completed",
                "bg-blue-50 text-blue-700 border border-blue-200 px-2.5 py-0.5 rounded-full text-xs font-medium",
            ),
            (
                "On Hold",
                "bg-gray-100 text-gray-600 border border-gray-200 px-2.5 py-0.5 rounded-full text-xs font-medium",
            ),
            "bg-gray-100 text-gray-600 border border-gray-200 px-2.5 py-0.5 rounded-full text-xs font-medium",
        ),
    )


def project_row(project: Project) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    rx.icon("folder", class_name="w-5 h-5 text-[#0284c7]"),
                    class_name="w-10 h-10 rounded-full bg-[#0284c7]/10 flex items-center justify-center mr-3",
                ),
                rx.el.div(
                    rx.el.p(
                        project["name"],
                        class_name="text-sm font-semibold text-gray-900",
                    ),
                    rx.el.p(project["created_at"], class_name="text-xs text-gray-500"),
                    class_name="flex flex-col",
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.p(
                    project["description"],
                    class_name="text-sm text-gray-600 truncate max-w-xs",
                )
            ),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            rx.el.div(
                rx.icon("user", class_name="w-3 h-3 mr-1 text-gray-400"),
                rx.el.span(
                    f"Owner ID: {project['owner_id']}",
                    class_name="text-sm text-gray-600",
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            status_badge(project["status"]), class_name="px-6 py-4 whitespace-nowrap"
        ),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon("pencil", class_name="w-4 h-4"),
                    on_click=lambda: ProjectState.edit_project(project),
                    class_name="p-1.5 text-[#0284c7] hover:bg-[#0284c7]/10 rounded-md transition-colors",
                    title="Edit",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="w-4 h-4"),
                    on_click=lambda: ProjectState.prompt_delete(project),
                    class_name="p-1.5 text-red-600 hover:bg-red-50 rounded-md transition-colors",
                    title="Delete",
                ),
                class_name="flex justify-end items-center gap-2",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        class_name="border-b border-gray-100 hover:bg-gray-50/80 transition-colors",
    )


def project_table() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "search",
                    class_name="w-5 h-5 text-gray-500 absolute left-4 top-1/2 -translate-y-1/2",
                ),
                rx.el.input(
                    placeholder="Search projects...",
                    on_change=ProjectState.set_project_search.debounce(300),
                    class_name="pl-12 pr-6 py-3 w-full sm:w-96 rounded-full border border-gray-200 focus:ring-4 focus:ring-[#0284c7]/10 focus:border-[#0284c7] outline-none transition-all text-[15px] bg-white shadow-sm hover:shadow-md",
                ),
                class_name="relative",
            ),
            rx.el.button(
                rx.icon("plus", class_name="w-5 h-5 mr-2.5"),
                "New Project",
                on_click=ProjectState.toggle_add_dialog,
                class_name="bg-[#0284c7] hover:bg-[#0270a9] text-white pl-5 pr-6 py-3 rounded-full text-[15px] font-bold shadow-[0_4px_14px_rgba(2,132,199,0.3)] hover:shadow-[0_6px_20px_rgba(2,132,199,0.4)] transition-all transform hover:-translate-y-0.5 active:translate-y-0 flex items-center",
            ),
            class_name="flex flex-col sm:flex-row justify-between items-center gap-4 mb-8",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Project",
                            class_name="px-8 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Description",
                            class_name="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Owner",
                            class_name="px-6 py-4 text-left text-xs font-bold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Status",
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
                    rx.foreach(ProjectState.filtered_projects, project_row),
                    class_name="bg-white divide-y divide-gray-100",
                ),
                class_name="min-w-full divide-y divide-gray-100",
            ),
            class_name="overflow-x-auto rounded-[24px] border border-gray-100 shadow-[0_4px_24px_rgba(0,0,0,0.04)] bg-white",
        ),
        rx.el.div(
            rx.el.p(
                f"Showing {ProjectState.filtered_projects.length()} of {ProjectState.total_projects} projects",
                class_name="text-sm font-medium text-gray-500",
            ),
            class_name="mt-6 px-4",
        ),
        class_name="w-full",
    )