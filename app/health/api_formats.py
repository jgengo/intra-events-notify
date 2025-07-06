from typing import Literal

from pydantic import BaseModel


class GetHealthResponse(BaseModel):
    status: Literal["OK"] = "OK"
