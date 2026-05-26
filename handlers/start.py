from pyrogram import Client, filters
from core.database import add_user
#@cantarellabots
def register_start(app: Client):
    @app.on_message(filters.command("start") & filters.private)
    async def start_handler(client, message):
        # Register user in DB
        await add_user(message.from_user.id, message.from_user.username)
        
        await message.reply_text(
            "👋 **Welcome to MediaInfo Bot!**\n\n"
            "Send me any Video, Audio, or Document (Media) to get Its technical details without downloading the full file.\n\n"
            "Powered by `MediaInfo` streaming technology."
        )
