import asyncio
import logging
from datetime import datetime, timedelta, timezone
from typing import List, Optional

from telegram import Bot
from telegram.error import TelegramError

from app.config import Config
from app.webhooks.api_formats import EventRequestV1

logger = logging.getLogger(__name__)


class TelegramClient:
    def __init__(self, config: Config):
        self.config = config
        self.bot = Bot(token=config.telegram_bot_token)
        self.chat_id = config.telegram_group_id

    def _format_event_dates(self, begin_at: str, end_at: str) -> str:
        try:
            helsinki_tz = timezone(timedelta(hours=2))

            begin_dt = datetime.strptime(begin_at, "%Y-%m-%d %H:%M:%S UTC")
            end_dt = datetime.strptime(end_at, "%Y-%m-%d %H:%M:%S UTC")

            begin_helsinki = begin_dt.astimezone(helsinki_tz)
            end_helsinki = end_dt.astimezone(helsinki_tz)

            duration = end_helsinki - begin_helsinki

            date_str = begin_helsinki.strftime("%A, %B %d")
            time_str = begin_helsinki.strftime("%H:%M")

            hours = int(duration.total_seconds() // 3600)
            minutes = int((duration.total_seconds() % 3600) // 60)

            if hours > 0 and minutes > 0:
                duration_str = f"{hours}h {minutes}m"
            elif hours > 0:
                duration_str = f"{hours}h"
            else:
                duration_str = f"{minutes}m"

            return f"{date_str} at {time_str} ({duration_str})"
        except Exception as e:
            logger.error(f"Error formatting dates: {e}")
            return f"{begin_at} - {end_at}"

    async def send_message(self, text: str, parse_mode: Optional[str] = None) -> bool:
        try:
            await self.bot.send_message(
                chat_id=self.chat_id, text=text, parse_mode=parse_mode
            )
            logger.info(f"Message sent successfully to chat {self.chat_id}")
            return True
        except TelegramError as e:
            logger.error(f"Failed to send Telegram message: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending Telegram message: {e}")
            return False

    async def send_messages(
        self, messages: List[str], parse_mode: Optional[str] = None
    ) -> int:
        if not messages:
            logger.warning("No messages provided to send")
            return 0

        successful_sends = 0
        for i, message in enumerate(messages):
            try:
                await self.bot.send_message(
                    chat_id=self.chat_id, text=message, parse_mode=parse_mode
                )
                successful_sends += 1
                logger.info(f"Message {i+1}/{len(messages)} sent successfully")

                if i < len(messages) - 1:
                    await asyncio.sleep(0.1)

            except TelegramError as e:
                logger.error(f"Failed to send message {i+1}/{len(messages)}: {e}")
            except Exception as e:
                logger.error(
                    f"Unexpected error sending message {i+1}/{len(messages)}: {e}"
                )

        logger.info(f"Sent {successful_sends}/{len(messages)} messages successfully")
        return successful_sends

    async def send_event_notification(self, event: EventRequestV1) -> bool:
        message = f"<b>{event.name}</b>"

        if event.begin_at and event.end_at:
            message += (
                f"\n\n📅    {self._format_event_dates(event.begin_at, event.end_at)}"
            )

        if event.location:
            message += f"\n📍    {event.location}"

        if event.max_people:
            message += f"\n👥    Max <b>{event.max_people} people</b>"

        if event.description:
            escaped_description = event.description.replace("<", "&lt;").replace(
                ">", "&gt;"
            )
            message += f"\n\n<code>{escaped_description}</code>"

        message += f"\n\n&gt;&gt;&gt; <a href='https://profile.intra.42.fr/events/{event.id}'>Register</a> &lt;&lt;&lt;"

        return await self.send_message(message, parse_mode="HTML")

    async def test_connection(self) -> bool:
        try:
            bot_info = await self.bot.get_me()
            logger.info(f"Telegram bot connection successful: {bot_info.first_name}")
            return True
        except TelegramError as e:
            logger.error(f"Telegram bot connection failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error testing Telegram connection: {e}")
            return False

    async def close(self):
        try:
            await self.bot.close()
            logger.info("Telegram bot session closed")
        except Exception as e:
            logger.error(f"Error closing Telegram bot session: {e}")


async def main(config: Config):
    client = TelegramClient(config)

    try:
        if await client.test_connection():
            messages = [
                "Don't forget to visit https://jgengo.fr",
                "And the cool herbarium on https://jgengo.fr/herbarium!",
            ]

            await client.send_messages(messages)
        else:
            logger.error("Failed to establish Telegram connection")
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main(config=Config()))
