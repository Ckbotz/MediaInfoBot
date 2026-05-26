from pyrogram import Client, filters
from config import OWNER_ID
from core.database import get_all_users_count, ban_user, unban_user, add_admin, is_admin
#@cantarellabots
def register_admin_handlers(app: Client):

    @app.on_message(filters.command("users") & filters.private)
    async def users_count_handler(client, message):
        if not await is_admin(message.from_user.id, OWNER_ID):
            return
        count = await get_all_users_count()
        await message.reply_text(f"📊 **Total Users**: `{count}`")

    @app.on_message(filters.command("ban") & filters.private)
    async def ban_handler(client, message):
        if not await is_admin(message.from_user.id, OWNER_ID):
            return
        
        user_id = None
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
        elif len(message.command) > 1:
            try:
                user_id = int(message.command[1])
            except ValueError:
                return await message.reply_text("❌ Please provide a valid User ID.")
        
        if not user_id:
            return await message.reply_text("❌ Reply to a user or provide a User ID to ban.")
        
        await ban_user(user_id)
        await message.reply_text(f"🚫 **User banned**: `{user_id}`")

    @app.on_message(filters.command("unban") & filters.private)
    async def unban_handler(client, message):
        if not await is_admin(message.from_user.id, OWNER_ID):
            return
        
        if len(message.command) < 2:
            return await message.reply_text("❌ Please provide a User ID to unban.")
        
        try:
            user_id = int(message.command[1])
        except ValueError:
            return await message.reply_text("❌ Please provide a valid User ID.")
            
        await unban_user(user_id)
        await message.reply_text(f"✅ **User unbanned**: `{user_id}`")

    @app.on_message(filters.command("add_admin") & filters.private)
    async def add_admin_handler(client, message):
        if message.from_user.id != OWNER_ID:
            return await message.reply_text("❌ Only the Owner can add admins.")
        
        user_id = None
        if message.reply_to_message:
            user_id = message.reply_to_message.from_user.id
        elif len(message.command) > 1:
            try:
                user_id = int(message.command[1])
            except ValueError:
                return await message.reply_text("❌ Please provide a valid User ID.")
        
        if not user_id:
            return await message.reply_text("❌ Reply to a user or provide a User ID.")
            
        await add_admin(user_id)
        await message.reply_text(f"👑 **Admin added**: `{user_id}`")
