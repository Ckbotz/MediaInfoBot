#@cantarellabots
import io
from pyrogram import Client, filters
from core.telegram_file import get_file_url
from core.mediainfo import extract_mediainfo
from core.formatter import format_output
from core.database import is_banned
#@cantarellabots
def register_media_handler(app: Client):

    @app.on_message((filters.video | filters.audio | filters.document) & filters.private)
    async def media_handler(client, message):
        # Check if user is banned
        if await is_banned(message.from_user.id):
            return await message.reply_text("❌ **You are banned from using this bot.**")
        # Determine media type for a better UX
        media = message.video or message.audio or message.document
        
        # If it's a document, check if it's a media file might be overkill but good for safety
        # For now, we follow the prompt's filter
        
        status_msg = await message.reply_text("🔍 **Extracting MediaInfo...**\n*This may take a few seconds as I probe the header.*")
        
        try:
            # 1. Get Streaming URL (Local)
            url = await get_file_url(message.chat.id, message.id)
            
            # 2. Extract Metadata via Streaming Probe
            data = await extract_mediainfo(url)
            
            # 3. Format Output
            text = format_output(data)
            
            # 4. Send Result
            full_text = f"📊 **MediaInfo for**: `{media.file_name or 'File'}`\n\n{text}"
            if len(full_text) > 4096:
                clean_text = text.replace("```", "").strip()
                bio = io.BytesIO(clean_text.encode("utf-8"))
                bio.name = f"{media.file_name or 'mediainfo'}.txt"
                
                await status_msg.edit_text(
                    f"📊 **MediaInfo for**: `{media.file_name or 'File'}` is too long to display inline. "
                    "Sending detailed report as a text file..."
                )
                await message.reply_document(
                    document=bio,
                    caption=f"📊 **MediaInfo for**: `{media.file_name or 'File'}`"
                )
            else:
                await status_msg.edit_text(full_text)
            
        except Exception as e:
            await status_msg.edit_text(f"❌ **Error**: `{str(e)}`")
