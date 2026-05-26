from pyrogram import Client
import logging
from config import API_ID, API_HASH, BOT_TOKEN
from handlers.media_handler import register_media_handler
from handlers.start import register_start
from handlers.admin import register_admin_handlers
from core.streamer import MediaStreamer
import asyncio
from aiohttp import web

# @cantarellabots

# Setup logging
logging.basicConfig(level=logging.INFO)

# @cantarellabots

app = Client(
    "mediainfo_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


# Health check handler for Koyeb
async def health_check(request):
    return web.Response(text="OK", status=200)


async def start_health_server():
    web_app = web.Application()
    web_app.router.add_get("/", health_check)
    web_app.router.add_get("/health", health_check)
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()
    logging.info("Health check server running on port 8080")


async def main():
    # Start health check server for Koyeb
    await start_health_server()

    # Start Bot
    await app.start()

    # Start Streamer
    streamer = MediaStreamer(app)
    await streamer.start()

    # Register Handlers
    register_start(app)
    register_admin_handlers(app)
    register_media_handler(app)

    print("Bot is running...")
    await asyncio.Event().wait()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
