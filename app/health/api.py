from fastapi import APIRouter

from app.health.api_formats import GetHealthResponse


def create_health_router():
    router = APIRouter()

    @router.get("/", response_model=GetHealthResponse, tags=["Health"])
    @router.get("/health", response_model=GetHealthResponse, tags=["Health"])
    async def get_health() -> GetHealthResponse:
        get_health_response = GetHealthResponse(status="OK")

        return get_health_response

    return router
