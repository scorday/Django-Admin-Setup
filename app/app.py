import reflex as rx
from app.pages.dashboard import dashboard_page
from app.pages.users import users_page
from app.pages.projects import projects_page

app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700;900&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(dashboard_page, route="/")
app.add_page(users_page, route="/users")
app.add_page(projects_page, route="/projects")