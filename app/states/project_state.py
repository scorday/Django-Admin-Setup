import reflex as rx
import datetime
from app.models import Project


class ProjectState(rx.State):
    projects: list[Project] = [
        {
            "id": 101,
            "name": "Q4 Marketing Campaign",
            "description": "End of year digital marketing push focusing on social media channels.",
            "owner_id": 2,
            "status": "Active",
            "created_at": "2023-12-01",
        },
        {
            "id": 102,
            "name": "Website Redesign",
            "description": "Complete overhaul of the corporate website with new branding.",
            "owner_id": 1,
            "status": "On Hold",
            "created_at": "2024-01-05",
        },
        {
            "id": 103,
            "name": "Mobile App Launch",
            "description": "Deployment of the new iOS and Android applications.",
            "owner_id": 4,
            "status": "Completed",
            "created_at": "2023-11-20",
        },
        {
            "id": 104,
            "name": "Data Migration",
            "description": "Transferring legacy data to the new cloud infrastructure.",
            "owner_id": 1,
            "status": "Active",
            "created_at": "2024-02-01",
        },
    ]
    next_project_id: int = 105
    project_search_query: str = ""
    is_add_open: bool = False
    is_edit_open: bool = False
    is_delete_open: bool = False
    current_project_id: int = 0
    form_name: str = ""
    form_description: str = ""
    form_owner_id: str = "1"
    form_status: str = "Active"
    form_error: str = ""
    user_options: list[dict[str, str]] = [
        {"label": "Alexandra Chen", "value": "1"},
        {"label": "Marcus Johnson", "value": "2"},
        {"label": "Sarah Miller", "value": "3"},
        {"label": "James Wilson", "value": "4"},
        {"label": "Emily Zhang", "value": "5"},
    ]

    @rx.var
    def total_projects(self) -> int:
        return len(self.projects)

    @rx.var
    def active_projects_count(self) -> int:
        return len([p for p in self.projects if p["status"] == "Active"])

    @rx.var
    def filtered_projects(self) -> list[Project]:
        if not self.project_search_query:
            return self.projects
        query = self.project_search_query.lower()
        return [
            p
            for p in self.projects
            if query in p["name"].lower() or query in p["description"].lower()
        ]

    @rx.var
    def active_projects_list(self) -> list[Project]:
        return [p for p in self.projects if p["status"] == "Active"]

    @rx.event
    def get_owner_name(self, owner_id: int) -> str:
        for user in self.user_options:
            if user["value"] == str(owner_id):
                return user["label"]
        return "Unknown"

    @rx.event
    def validate_form(self) -> bool:
        if not self.form_name:
            self.form_error = "Project name is required"
            return False
        if not self.form_description:
            self.form_error = "Description is required"
            return False
        self.form_error = ""
        return True

    @rx.event
    def toggle_add_dialog(self):
        self.is_add_open = not self.is_add_open
        self.form_name = ""
        self.form_description = ""
        self.form_owner_id = "1"
        self.form_status = "Active"
        self.form_error = ""

    @rx.event
    def save_new_project(self):
        if not self.validate_form():
            return rx.toast.error(self.form_error)
        new_project: Project = {
            "id": self.next_project_id,
            "name": self.form_name,
            "description": self.form_description,
            "owner_id": int(self.form_owner_id),
            "status": self.form_status,
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d"),
        }
        self.projects.append(new_project)
        self.next_project_id += 1
        self.is_add_open = False
        return rx.toast.success(f"Project '{self.form_name}' initialized")

    @rx.event
    def edit_project(self, project: Project):
        self.current_project_id = project["id"]
        self.form_name = project["name"]
        self.form_description = project["description"]
        self.form_owner_id = str(project["owner_id"])
        self.form_status = project["status"]
        self.form_error = ""
        self.is_edit_open = True

    @rx.event
    async def save_edited_project(self):
        if not self.validate_form():
            return rx.toast.error(self.form_error)
        new_projects = []
        for p in self.projects:
            if p["id"] == self.current_project_id:
                p["name"] = self.form_name
                p["description"] = self.form_description
                p["owner_id"] = int(self.form_owner_id)
                p["status"] = self.form_status
            new_projects.append(p)
        self.projects = new_projects
        from app.states.rubric_state import RubricState

        rubric_state = await self.get_state(RubricState)
        rubric_state.handle_project_update(self.current_project_id, self.form_name)
        self.is_edit_open = False
        return rx.toast.success("Project updated successfully")

    @rx.event
    def cancel_edit(self):
        self.is_edit_open = False

    @rx.event
    def prompt_delete(self, project: Project):
        self.current_project_id = project["id"]
        self.form_name = project["name"]
        self.is_delete_open = True

    @rx.event
    async def confirm_delete(self):
        from app.states.rubric_state import RubricState

        rubric_state = await self.get_state(RubricState)
        rubric_state.handle_project_deletion(self.current_project_id)
        self.projects = [p for p in self.projects if p["id"] != self.current_project_id]
        self.is_delete_open = False
        return rx.toast.info("Project deleted")

    @rx.event
    def cancel_delete(self):
        self.is_delete_open = False

    @rx.event
    def update_project_status(self, project_id: int, new_status: str):
        new_projects = []
        for p in self.projects:
            if p["id"] == project_id:
                p["status"] = new_status
            new_projects.append(p)
        self.projects = new_projects
        return rx.toast.success("Project status updated")

    @rx.event
    def delete_project(self, project_id: int):
        self.projects = [p for p in self.projects if p["id"] != project_id]
        return rx.toast.info("Project removed")

    @rx.event
    def set_project_search(self, query: str):
        self.project_search_query = query

    @rx.event
    def set_form_name(self, value: str):
        self.form_name = value

    @rx.event
    def set_form_description(self, value: str):
        self.form_description = value

    @rx.event
    def set_form_owner_id(self, value: str):
        self.form_owner_id = value

    @rx.event
    def set_form_status(self, value: str):
        self.form_status = value