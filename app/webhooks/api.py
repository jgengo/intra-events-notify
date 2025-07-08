import logging
from enum import Enum
from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Request

from app.config import Config
from app.services.telegram_client import TelegramClient
from app.webhooks.api_formats import EventRequestV1, EventResponseV1, WebhookEvent

logger = logging.getLogger(__name__)


def _parse_headers(request: Request, config: Config) -> tuple[WebhookEvent, str]:
    secret = request.headers.get("X-Secret")
    if secret != config.webhook_secret:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    model = request.headers.get("X-Model")
    if model != "event":
        logger.info("Ignoring webhook for model: %s", model)
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)

    raw_event = request.headers.get("X-Event") or ""
    try:
        event = WebhookEvent(raw_event)
    except ValueError:
        logger.info("Ignoring webhook for event: %s", raw_event)
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)

    delivery_id = request.headers.get("X-Delivery", "N/A")

    return event, delivery_id


def create_webhook_router(config: Config, telegram_client: TelegramClient) -> APIRouter:
    router = APIRouter()

    @router.post(
        "/webhooks/events",
        tags=["Webhooks"],
        response_model=EventResponseV1,
        responses={
            HTTPStatus.UNAUTHORIZED: {"description": "Unauthorized"},
            HTTPStatus.BAD_REQUEST: {"description": "Invalid webhook payload or unsupported event type"},
        },
    )
    async def process_event(request: Request, event_data: EventRequestV1) -> EventResponseV1:
        try:
            event, delivery_id = _parse_headers(request, config)

            logger.warning("Processing webhook - Delivery: %s, Event: %s", delivery_id, event)
            logger.warning("Webhook payload: %s", event_data)

            if event is WebhookEvent.CREATE:
                await telegram_client.send_event_notification(event_data)
            else:  # WebhookEvent.DESTROY
                await telegram_client.send_event_deletion_notification(event_data)

            return EventResponseV1()

        except HTTPException:
            raise
        except Exception as exc:  # noqa: BLE001
            logger.error("Failed to process webhook: %s", exc)
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Failed to process event: {exc}",
            )

    return router
