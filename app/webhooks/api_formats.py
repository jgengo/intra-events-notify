from typing import Literal

from pydantic import BaseModel


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
