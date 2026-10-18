import asyncio
import logging

import aiohttp
from pyrogram.errors import FloodWait

from . import app
from .config import API_ID, API_HASH, BOT_TOKEN
from .health import start_health_server
from .queue import worker

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("skr_bot")


def validate_config():
    missing = []
    if not API_ID:
        missing.append("API_ID")
    if not API_HASH:
        missing.append("API_HASH")
    if not BOT_TOKEN:
        missing.append("BOT_TOKEN")
    if missing:
        raise RuntimeError("Missing required environment variables: " + ", ".join(missing))


async def clear_webhook_if_configured():
    """Remove a Bot API webhook if one exists, preserving pending updates."""
    api_base = f"https://api.telegram.org/bot{BOT_TOKEN}"
    timeout = aiohttp.ClientTimeout(total=15)
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(f"{api_base}/getWebhookInfo") as response:
                info = await response.json(content_type=None)
            if not info.get("ok"):
                logger.warning("Could not check Telegram webhook status: %s", info.get("description", "unknown error"))
                return
            webhook_url = (info.get("result") or {}).get("url", "")
            if not webhook_url:
                logger.info("Telegram Bot API webhook is not configured")
                return
            logger.warning("A Telegram Bot API webhook is configured; removing it while preserving pending updates")
            async with session.get(
                f"{api_base}/deleteWebhook",
                params={"drop_pending_updates": "false"},
            ) as response:
                result = await response.json(content_type=None)
            if result.get("ok"):
                logger.info("Telegram webhook removed successfully; pending updates were preserved")
            else:
                logger.error("Failed to remove Telegram webhook: %s", result.get("description", "unknown error"))
    except Exception as exc:
        # Never log request URLs because they contain the bot token.
        logger.warning("Could not check/remove Telegram webhook (%s); continuing startup", type(exc).__name__)


async def start_telegram_with_retry():
    """Wait out Telegram's temporary login rate limit instead of crash-looping."""
    while True:
        try:
            await app.start()
            return
        except FloodWait as exc:
            wait_seconds = int(getattr(exc, "value", 0) or 0) + 5
            wait_seconds = max(wait_seconds, 5)
            logger.warning(
                "Telegram login is rate-limited; will retry in %s seconds. Do not repeatedly restart this service.",
                wait_seconds,
            )
            await asyncio.sleep(wait_seconds)


async def main():
    try:
        validate_config()
        await clear_webhook_if_configured()
        await start_health_server()
        logger.info("Health server started")
        logger.info("Starting Telegram client...")
        await start_telegram_with_retry()
        me = await app.get_me()
        logger.info("Telegram connected as @%s (id=%s)", me.username, me.id)
        asyncio.create_task(worker(), name="skr-queue-worker")
        logger.info("SKR Bot started and ready to receive messages")
        await asyncio.Event().wait()
    except Exception:
        logger.exception("SKR Bot startup/runtime failure")
        raise
    finally:
        if app.is_connected:
            await app.stop()


if __name__ == "__main__":
    asyncio.run(main())
