import reflex as rx
from typing import TypedDict, Literal


class User(TypedDict):
    id: int
    name: str
    email: str
    role: str
    created_at: str
    is_active: bool


class Project(TypedDict):
    id: int
    name: str
    description: str
    owner_id: int
    status: str
    created_at: str


class Rubric(TypedDict):
    id: int
    project_id: int
    project_name: str
    name: str
    kql_query: str