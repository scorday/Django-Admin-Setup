import reflex as rx
from app.states.user_state import UserState
from app.states.project_state import ProjectState
from app.models import User, Project
from app.components.sidebar import sidebar


def stat_card(title: str, value: rx.Var, icon: str, color: str) -> rx.Component:
    colors = {
        "sky": ("text-sky-600", "bg-sky-50"),
        "green": ("text-green-600", "bg-green-50"),
        "blue": ("text-blue-600", "bg-blue-50"),
        "purple": ("text-purple-600", "bg-purple-50"),
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


def recent_user_row(user: User) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    user["name"][0], class_name="text-sm font-bold text-[#0284c7]"
                ),
                class_name="w-10 h-10 rounded-full bg-[#0284c7]/10 flex items-center justify-center mr-4 shadow-sm",
            ),
            rx.el.div(
                rx.el.p(
                    user["name"], class_name="text-[15px] font-semibold text-gray-900"
                ),
                rx.el.p(user["email"], class_name="text-xs text-gray-500 mt-0.5"),
                class_name="flex flex-col",
            ),
            class_name="flex items-center flex-1",
        ),
        rx.el.div(
            rx.el.span(
                user["role"],
                class_name="px-3 py-1 bg-gray-100 text-gray-700 text-xs rounded-full font-medium border border-gray-200",
            ),
            class_name="w-auto",
        ),
        class_name="flex items-center justify-between p-5 hover:bg-gray-50/80 transition-colors border-b last:border-0 border-gray-100/50",
    )


def project_card(project: Project) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h4(
                project["name"],
                class_name="font-bold text-gray-900 font-['Lato'] text-lg leading-tight",
            ),
            rx.el.span(
                project["status"],
                class_name=rx.cond(
                    project["status"] == "Active",
                    "bg-green-50 text-green-700 px-3 py-1 rounded-full text-xs font-bold border border-green-200",
                    rx.cond(
                        project["status"] == "Completed",
                        "bg-blue-50 text-blue-700 px-3 py-1 rounded-full text-xs font-bold border border-blue-200",
                        "bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-xs font-bold border border-gray-200",
                    ),
                ),
            ),
            class_name="flex justify-between items-start mb-3 gap-4",
        ),
        rx.el.p(
            project["description"],
            class_name="text-sm text-gray-600 line-clamp-2 mb-5 leading-relaxed",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("calendar", class_name="w-4 h-4 mr-2 text-gray-400"),
                rx.el.span(
                    project["created_at"],
                    class_name="text-xs font-medium text-gray-500",
                ),
                class_name="flex items-center",
            ),
            rx.el.div(
                rx.el.span("Owner ID: ", class_name="text-xs text-gray-400 mr-1.5"),
                rx.el.span(
                    project["owner_id"],
                    class_name="text-xs font-bold text-gray-700 bg-gray-100 px-2 py-0.5 rounded-md",
                ),
                class_name="flex items-center",
            ),
            class_name="flex justify-between items-center border-t border-gray-100 pt-4",
        ),
        class_name="bg-white p-6 rounded-[20px] border border-gray-100 shadow-[0_2px_8px_rgba(0,0,0,0.04)] hover:shadow-[0_8px_24px_rgba(0,0,0,0.08)] transition-all duration-300 ease-[cubic-bezier(0.4,0,0.2,1)] hover:-translate-y-1 cursor-pointer",
    )


def dashboard_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "Dashboard Overview",
                        class_name="text-4xl font-black text-gray-900 mb-2 font-['Lato'] tracking-tight",
                    ),
                    rx.el.p(
                        "System status and recent activity.",
                        class_name="text-lg text-gray-500 mb-10 font-medium",
                    ),
                    class_name="mb-8",
                ),
                rx.el.div(
                    stat_card(
                        "Total Users", UserState.total_users.to_string(), "users", "sky"
                    ),
                    stat_card(
                        "Active Users",
                        UserState.active_users_count.to_string(),
                        "user-check",
                        "green",
                    ),
                    stat_card(
                        "Total Projects",
                        ProjectState.total_projects.to_string(),
                        "folder",
                        "blue",
                    ),
                    stat_card(
                        "Active Projects",
                        ProjectState.active_projects_count.to_string(),
                        "activity",
                        "purple",
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-12",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.h2(
                                "Recent Users",
                                class_name="text-2xl font-bold text-gray-900 font-['Lato'] tracking-tight",
                            ),
                            rx.el.a(
                                rx.el.button(
                                    "View All",
                                    class_name="text-sm text-[#0284c7] hover:text-[#006090] font-bold transition-colors uppercase tracking-wide px-4 py-2 hover:bg-[#0284c7]/5 rounded-full",
                                ),
                                href="/users",
                            ),
                            class_name="flex justify-between items-center mb-6 pl-1",
                        ),
                        rx.el.div(
                            rx.foreach(UserState.recent_users, recent_user_row),
                            class_name="bg-white rounded-[24px] border border-gray-100/80 shadow-[0_4px_20px_rgba(0,0,0,0.03)] overflow-hidden",
                        ),
                        class_name="flex flex-col",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.h2(
                                "Active Projects",
                                class_name="text-2xl font-bold text-gray-900 font-['Lato'] tracking-tight",
                            ),
                            rx.el.button(
                                rx.icon("filter", class_name="w-4 h-4 mr-2"),
                                "Filter",
                                class_name="text-sm text-gray-600 hover:text-[#0284c7] flex items-center transition-colors font-medium px-4 py-2 hover:bg-gray-100 rounded-full",
                            ),
                            class_name="flex justify-between items-center mb-6 pl-1",
                        ),
                        rx.el.div(
                            rx.foreach(ProjectState.active_projects_list, project_card),
                            class_name="flex flex-col gap-6",
                        ),
                        class_name="flex flex-col",
                    ),
                    class_name="grid grid-cols-1 xl:grid-cols-2 gap-10",
                ),
                class_name="max-w-screen-2xl mx-auto",
            ),
            class_name="lg:ml-[280px] p-8 lg:p-12 min-h-screen bg-[#f8f9fa]",
        ),
        class_name="font-['Lato'] text-gray-900 bg-[#f8f9fa] min-h-screen",
    )