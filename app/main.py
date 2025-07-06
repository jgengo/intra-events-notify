from contextlib import asynccontextmanager
from http import HTTPStatus
from typing import AsyncIterator

from fastapi import APIRouter, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.config import Config
from app.health.api import create_health_router


async def create_routers() -> list[APIRouter]:

    return [
        create_health_router(),
    ]


def create_api(config: Config, do_enable_lifespan: bool = True) -> FastAPI:
    @asynccontextmanager
    async def lifespan(_api: FastAPI) -> AsyncIterator[None]:
        for router in await create_routers():
            api.include_router(router)

        yield

    api = FastAPI(
        title="Intra Events Telegram", lifespan=lifespan if do_enable_lifespan else None
    )

    @api.exception_handler(ValidationError)
    async def exception_handler_validation_error(
        _: Request, exc: ValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST, content={"details": str(exc)}
        )

    @api.exception_handler(HTTPException)
    async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code, content={"message": exc.detail}
        )

    return api


if __name__ in {"app.main", "main"}:
    app = create_api(config=Config())
