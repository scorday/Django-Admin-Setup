import reflex as rx
from app.models import Rubric
from app.states.project_state import ProjectState


class RubricState(rx.State):
    rubrics: list[Rubric] = [
        {
            "id": 1,
            "project_id": 101,
            "project_name": "Q4 Marketing Campaign",
            "name": "High Engagement",
            "kql_query": "engagement > 1000",
        },
        {
            "id": 2,
            "project_id": 101,
            "project_name": "Q4 Marketing Campaign",
            "name": "Viral Posts",
            "kql_query": "shares > 500 AND likes > 2000",
        },
        {
            "id": 3,
            "project_id": 101,
            "project_name": "Q4 Marketing Campaign",
            "name": "Negative Feedback",
            "kql_query": "sentiment < 0.2",
        },
        {
            "id": 4,
            "project_id": 102,
            "project_name": "Website Redesign",
            "name": "Homepage Errors",
            "kql_query": "page == 'home' AND status >= 500",
        },
        {
            "id": 5,
            "project_id": 102,
            "project_name": "Website Redesign",
            "name": "Slow Load Times",
            "kql_query": "latency > 2000ms",
        },
        {
            "id": 6,
            "project_id": 102,
            "project_name": "Website Redesign",
            "name": "Broken Links",
            "kql_query": "status == 404",
        },
        {
            "id": 7,
            "project_id": 103,
            "project_name": "Mobile App Launch",
            "name": "Crash Reports",
            "kql_query": "event == 'crash'",
        },
        {
            "id": 8,
            "project_id": 103,
            "project_name": "Mobile App Launch",
            "name": "New Signups",
            "kql_query": "event == 'signup_success'",
        },
        {
            "id": 9,
            "project_id": 103,
            "project_name": "Mobile App Launch",
            "name": "Active Sessions",
            "kql_query": "session_duration > 60",
        },
        {
            "id": 10,
            "project_id": 104,
            "project_name": "Data Migration",
            "name": "Failed Transfers",
            "kql_query": "status == 'transfer_failed'",
        },
        {
            "id": 11,
            "project_id": 104,
            "project_name": "Data Migration",
            "name": "Data Integrity",
            "kql_query": "checksum_match == false",
        },
        {
            "id": 12,
            "project_id": 104,
            "project_name": "Data Migration",
            "name": "Orphaned Records",
            "kql_query": "parent_id == null AND type == 'child'",
        },
        {
            "id": 13,
            "project_id": 101,
            "project_name": "Q4 Marketing Campaign",
            "name": "Bot Traffic",
            "kql_query": "user_agent contains 'bot' AND requests > 100",
        },
        {
            "id": 14,
            "project_id": 104,
            "project_name": "Data Migration",
            "name": "Schema Mismatch",
            "kql_query": "error_type == 'schema_validation'",
        },
    ]
    next_rubric_id: int = 15
    search_query: str = ""
    filter_project_id: str = "All"
    is_add_open: bool = False
    is_edit_open: bool = False
    is_delete_open: bool = False
    current_rubric_id: int = 0
    form_name: str = ""
    form_kql_query: str = ""
    form_project_id: str = ""
    form_error: str = ""

    @rx.var
    def total_rubrics(self) -> int:
        return len(self.rubrics)

    @rx.var
    def unique_projects_count(self) -> int:
        return len(set((r["project_id"] for r in self.rubrics)))

    @rx.var
    def filtered_rubrics(self) -> list[Rubric]:
        items = self.rubrics
        if self.filter_project_id != "All":
            items = [r for r in items if str(r["project_id"]) == self.filter_project_id]
        if self.search_query:
            query = self.search_query.lower()
            items = [
                r
                for r in items
                if query in r["name"].lower()
                or query in r["kql_query"].lower()
                or query in r["project_name"].lower()
            ]
        return items

    @rx.event
    def validate_form(self) -> bool:
        if not self.form_name:
            self.form_error = "Rubric name is required"
            return False
        if not self.form_kql_query:
            self.form_error = "KQL query is required"
            return False
        if not self.form_project_id:
            self.form_error = "Project selection is required"
            return False
        self.form_error = ""
        return True

    @rx.event
    def toggle_add_dialog(self):
        self.is_add_open = not self.is_add_open
        self.form_name = ""
        self.form_kql_query = ""
        self.form_project_id = ""
        self.form_error = ""

    @rx.event
    async def save_new_rubric(self):
        if not self.validate_form():
            return rx.toast.error(self.form_error)
        project_state = await self.get_state(ProjectState)
        project_name = "Unknown Project"
        for p in project_state.projects:
            if str(p["id"]) == self.form_project_id:
                project_name = p["name"]
                break
        new_rubric: Rubric = {
            "id": self.next_rubric_id,
            "project_id": int(self.form_project_id),
            "project_name": project_name,
            "name": self.form_name,
            "kql_query": self.form_kql_query,
        }
        self.rubrics.append(new_rubric)
        self.next_rubric_id += 1
        self.is_add_open = False
        return rx.toast.success(f"Rubric '{self.form_name}' created")

    @rx.event
    def edit_rubric(self, rubric: Rubric):
        self.current_rubric_id = rubric["id"]
        self.form_name = rubric["name"]
        self.form_kql_query = rubric["kql_query"]
        self.form_project_id = str(rubric["project_id"])
        self.form_error = ""
        self.is_edit_open = True

    @rx.event
    async def save_edited_rubric(self):
        if not self.validate_form():
            return rx.toast.error(self.form_error)
        project_state = await self.get_state(ProjectState)
        project_name = "Unknown Project"
        for p in project_state.projects:
            if str(p["id"]) == self.form_project_id:
                project_name = p["name"]
                break
        new_rubrics = []
        for r in self.rubrics:
            if r["id"] == self.current_rubric_id:
                r["name"] = self.form_name
                r["kql_query"] = self.form_kql_query
                r["project_id"] = int(self.form_project_id)
                r["project_name"] = project_name
            new_rubrics.append(r)
        self.rubrics = new_rubrics
        self.is_edit_open = False
        return rx.toast.success("Rubric updated successfully")

    @rx.event
    def cancel_edit(self):
        self.is_edit_open = False

    @rx.event
    def prompt_delete(self, rubric: Rubric):
        self.current_rubric_id = rubric["id"]
        self.form_name = rubric["name"]
        self.is_delete_open = True

    @rx.event
    def confirm_delete(self):
        self.rubrics = [r for r in self.rubrics if r["id"] != self.current_rubric_id]
        self.is_delete_open = False
        return rx.toast.info("Rubric deleted")

    @rx.event
    def cancel_delete(self):
        self.is_delete_open = False

    @rx.event
    def duplicate_rubric(self, rubric: Rubric):
        new_rubric = rubric.copy()
        new_rubric["id"] = self.next_rubric_id
        self.next_rubric_id += 1
        new_rubric["name"] = f"{rubric['name']} (Copy)"
        self.rubrics.append(new_rubric)
        return rx.toast.success(f"Rubric '{rubric['name']}' duplicated")

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query

    @rx.event
    def set_filter_project_id(self, value: str):
        self.filter_project_id = value

    @rx.event
    def set_form_name(self, value: str):
        self.form_name = value

    @rx.event
    def set_form_kql_query(self, value: str):
        self.form_kql_query = value

    @rx.event
    def set_form_project_id(self, value: str):
        self.form_project_id = value

    @rx.event
    def handle_project_deletion(self, project_id: int):
        """Remove rubrics associated with a deleted project."""
        self.rubrics = [r for r in self.rubrics if r["project_id"] != project_id]

    @rx.event
    def handle_project_update(self, project_id: int, new_name: str):
        """Update project name in rubrics when the parent project is renamed."""
        new_rubrics = []
        for r in self.rubrics:
            if r["project_id"] == project_id:
                r["project_name"] = new_name
            new_rubrics.append(r)
        self.rubrics = new_rubrics