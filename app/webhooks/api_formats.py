from pydantic import BaseModel


class EventRequestV1(BaseModel):
    event_type: str  # e.g., "created", "deleted"
    title: str
    description: str | None = None
    start_time: str  # or datetime
    location: str | None = None
