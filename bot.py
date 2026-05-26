from pyrogram import Client
import logging
from config import API_ID, API_HASH, BOT_TOKEN
from handlers.media_handler import register_media_handler
from handlers.start import register_start
from handlers.admin import register_admin_handlers
from core.streamer import MediaStreamer
import asyncio
#@cantarellabots
# Setup logging
logging.basicConfig(level=logging.INFO)
#@cantarellabots
app = Client(
    "mediainfo_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

async def main():
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
