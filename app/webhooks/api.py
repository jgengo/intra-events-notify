import asyncio
from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from app.services.telegram_client import TelegramClient
from app.webhooks.api_formats import EventRequestV1


def create_webhook_router(telegram_client: TelegramClient):
    router = APIRouter()

    @router.post("/webhooks/events", tags=["Webhooks"])
    async def process_event(request: EventRequestV1):
        try:
            await telegram_client.send_event_notification(request)
            return {"status": "success", "message": "Event processed successfully"}
        except Exception as e:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Failed to process event: {str(e)}",
            )

    # TODO: remove in production, just for testing purpose
    @router.get("/webhooks", tags=["Webhooks"])
    async def get_webhooks():
        try:
            await telegram_client.send_message("test test")
            asyncio.sleep(0.01)
        except Exception as e:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail=f"Failed to send test message: {str(e)}",
            )

        return {"status": "OK"}

    return router
