from enum import Enum
from typing import Literal

from pydantic import BaseModel


class WebhookEvent(str, Enum):
    CREATE = "create"
    DESTROY = "destroy"


class EventRequestV1(BaseModel):
    id: int
    begin_at: str
    end_at: str
    name: str
    description: str | None = None
    location: str | None = None
    kind: str
    max_people: int | None = None
    prohibition_of_cancellation: bool | None = None
    campus_ids: list[int]
    cursus_ids: list[int]
    created_at: str
    updated_at: str


class EventResponseV1(BaseModel):
    status: Literal["success"] = "success"
    message: Literal["Event processed successfully"] = "Event processed successfully"


class ExamProject(BaseModel):
    """Information about a project available during an exam."""

    name: str
    id: int
    slug: str
    url: str


class ExamRequestV1(BaseModel):
    """Payload sent by the webhook when an exam is created or deleted."""

    id: int
    begin_at: str
    end_at: str
    location: str | None = None
    ip_range: str | None = None
    max_people: int | None = None
    visible: bool | None = None
    name: str
    campus_id: int
    created_at: str
    updated_at: str
    projects: list[ExamProject] | None = None


class ExamResponseV1(BaseModel):
    status: Literal["success"] = "success"
    message: Literal["Exam processed successfully"] = "Exam processed successfully"
