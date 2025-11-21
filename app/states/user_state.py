import reflex as rx
import datetime
from app.models import User


class UserState(rx.State):
    users: list[User] = [
        {
            "id": 1,
            "name": "Alexandra Chen",
            "email": "alex.chen@techcorp.com",
            "role": "Admin",
            "created_at": "2023-11-15",
            "is_active": True,
        },
        {
            "id": 2,
            "name": "Marcus Johnson",
            "email": "m.johnson@design.io",
            "role": "Editor",
            "created_at": "2023-12-02",
            "is_active": True,
        },
        {
            "id": 3,
            "name": "Sarah Miller",
            "email": "sarah.m@consulting.net",
            "role": "Viewer",
            "created_at": "2024-01-10",
            "is_active": False,
        },
        {
            "id": 4,
            "name": "James Wilson",
            "email": "j.wilson@dev.co",
            "role": "Editor",
            "created_at": "2024-01-25",
            "is_active": True,
        },
        {
            "id": 5,
            "name": "Emily Zhang",
            "email": "emily.z@analytics.ai",
            "role": "Viewer",
            "created_at": "2024-02-14",
            "is_active": True,
        },
    ]
    next_user_id: int = 6
    search_query: str = ""
    is_add_open: bool = False
    is_edit_open: bool = False
    is_delete_open: bool = False
    current_user_id: int = 0
    form_name: str = ""
    form_email: str = ""
    form_role: str = "Viewer"
    form_error: str = ""

    @rx.var
    def total_users(self) -> int:
        return len(self.users)

    @rx.var
    def active_users_count(self) -> int:
        return len([u for u in self.users if u["is_active"]])

    @rx.var
    def filtered_users(self) -> list[User]:
        if not self.search_query:
            return self.users
        query = self.search_query.lower()
        return [
            u
            for u in self.users
            if query in u["name"].lower() or query in u["email"].lower()
        ]

    @rx.var
    def recent_users(self) -> list[User]:
        return sorted(self.users, key=lambda u: u["id"], reverse=True)[:5]

    @rx.event
    def validate_form(self) -> bool:
        if not self.form_name or not self.form_email:
            self.form_error = "Name and Email are required"
            return False
        if "@" not in self.form_email or "." not in self.form_email:
            self.form_error = "Invalid email format"
            return False
        self.form_error = ""
        return True

    @rx.event
    def toggle_add_dialog(self):
        self.is_add_open = not self.is_add_open
        self.form_name = ""
        self.form_email = ""
        self.form_role = "Viewer"
        self.form_error = ""

    @rx.event
    def save_new_user(self):
        if not self.validate_form():
            return rx.toast.error(self.form_error)
        new_user: User = {
            "id": self.next_user_id,
            "name": self.form_name,
            "email": self.form_email,
            "role": self.form_role,
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d"),
            "is_active": True,
        }
        self.users.append(new_user)
        self.next_user_id += 1
        self.is_add_open = False
        return rx.toast.success(f"User {self.form_name} created successfully")

    @rx.event
    def edit_user(self, user: User):
        self.current_user_id = user["id"]
        self.form_name = user["name"]
        self.form_email = user["email"]
        self.form_role = user["role"]
        self.form_error = ""
        self.is_edit_open = True

    @rx.event
    def save_edited_user(self):
        if not self.validate_form():
            return rx.toast.error(self.form_error)
        new_users = []
        for u in self.users:
            if u["id"] == self.current_user_id:
                u["name"] = self.form_name
                u["email"] = self.form_email
                u["role"] = self.form_role
            new_users.append(u)
        self.users = new_users
        self.is_edit_open = False
        return rx.toast.success("User details updated")

    @rx.event
    def cancel_edit(self):
        self.is_edit_open = False

    @rx.event
    def prompt_delete(self, user: User):
        self.current_user_id = user["id"]
        self.form_name = user["name"]
        self.is_delete_open = True

    @rx.event
    def confirm_delete(self):
        self.users = [u for u in self.users if u["id"] != self.current_user_id]
        self.is_delete_open = False
        return rx.toast.info("User permanently deleted")

    @rx.event
    def cancel_delete(self):
        self.is_delete_open = False

    @rx.event
    def update_user_status(self, user_id: int, is_active: bool):
        new_users = []
        for u in self.users:
            if u["id"] == user_id:
                u["is_active"] = is_active
            new_users.append(u)
        self.users = new_users

    @rx.event
    def delete_user(self, user_id: int):
        self.users = [u for u in self.users if u["id"] != user_id]
        return rx.toast.info("User deleted")

    @rx.event
    def set_search(self, query: str):
        self.search_query = query

    @rx.event
    def set_form_name(self, value: str):
        self.form_name = value

    @rx.event
    def set_form_email(self, value: str):
        self.form_email = value

    @rx.event
    def set_form_role(self, value: str):
        self.form_role = value