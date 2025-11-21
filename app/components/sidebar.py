import reflex as rx


def sidebar_item(text: str, icon_name: str, href: str) -> rx.Component:
    current_path = rx.State.router.page.path
    is_active = rx.cond(
        href == "/", current_path == "/", current_path.contains(href.strip("/"))
    )
    return rx.el.a(
        rx.el.div(
            rx.icon(
                icon_name,
                class_name=rx.cond(
                    is_active, "text-[#0284c7] w-6 h-6", "text-gray-600 w-6 h-6"
                ),
            ),
            rx.el.span(text, class_name="ml-4 text-[15px] font-medium tracking-wide"),
            class_name=rx.cond(
                is_active,
                "flex items-center px-5 py-3.5 bg-[#0284c7]/15 text-[#0284c7] rounded-full mx-3 mb-1 transition-all duration-300 ease-[cubic-bezier(0.4,0,0.2,1)] font-bold shadow-sm",
                "flex items-center px-5 py-3.5 text-gray-600 hover:bg-gray-100/80 rounded-full mx-3 mb-1 transition-all duration-300 ease-[cubic-bezier(0.4,0,0.2,1)] hover:text-gray-900",
            ),
        ),
        href=href,
        class_name="block",
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon("layout-grid", class_name="w-8 h-8 text-[#0284c7]"),
                rx.el.span(
                    "AdminPanel",
                    class_name="font-extrabold text-2xl text-gray-900 ml-3 tracking-tight",
                ),
                class_name="flex items-center",
            ),
            class_name="flex items-center px-8 py-10 mb-4",
        ),
        rx.el.nav(
            sidebar_item("Dashboard", "layout-dashboard", "/"),
            sidebar_item("Users", "users", "/users"),
            sidebar_item("Projects", "folder-kanban", "/projects"),
            sidebar_item("Rubrics", "file-code", "/rubrics"),
            sidebar_item("Settings", "settings", "/settings"),
            class_name="flex flex-col gap-1.5",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.img(
                    src="https://api.dicebear.com/9.x/initials/svg?seed=Admin",
                    class_name="w-11 h-11 rounded-full bg-gray-100 shadow-sm",
                ),
                rx.el.div(
                    rx.el.p("Admin User", class_name="text-sm font-bold text-gray-900"),
                    rx.el.p(
                        "admin@system.com",
                        class_name="text-xs text-gray-500 font-medium mt-0.5",
                    ),
                    class_name="flex flex-col ml-3.5",
                ),
                class_name="flex items-center px-6 py-5 border-t border-gray-100 bg-gray-50/50",
            ),
            class_name="mt-auto",
        ),
        class_name="w-[280px] bg-white border-r border-gray-100 h-screen fixed left-0 top-0 flex flex-col z-50 font-['Lato'] hidden lg:flex shadow-[0_0_15px_rgba(0,0,0,0.03)]",
    )