import logging
from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Request

from app.config import Config
from app.services.telegram_client import TelegramClient
from app.webhooks.api_formats import EventRequestV1, EventResponseV1

logger = logging.getLogger(__name__)


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
            secret = request.headers.get("X-Secret")
            model = request.headers.get("X-Model")
            event = request.headers.get("X-Event")
            delivery_id = request.headers.get("X-Delivery")

            if not secret or secret != config.webhook_secret:
                raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

            if model != "event":
                logger.info("Ignoring webhook for model: %s", model)
                raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)

            if event not in ["create", "destroy"]:
                logger.info("Ignoring webhook for event: %s", event)
                raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)

            logger.warning(
                "Processing webhook - Delivery: %s, Model: %s, Event: %s",
                delivery_id,
                model,
                event,
            )
            logger.warning("New webhook received: %s", event_data)

            if event == "create":
                await telegram_client.send_event_notification(event_data)
            elif event == "destroy":
                await telegram_client.send_event_deletion_notification(event_data)

            return EventResponseV1(status="success", message="Event processed successfully")

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Failed to process webhook: %s", str(e))
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Failed to process event: {str(e)}",
            )

    return router
