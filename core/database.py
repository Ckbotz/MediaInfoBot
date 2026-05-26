from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI
#@cantarellabots
client = AsyncIOMotorClient(MONGO_URI)
db = client.mediainfo_bot
#@cantarellabots
users_db = db.users
admins_db = db.admins

async def add_user(user_id, username):
    await users_db.update_one(
        {"user_id": user_id},
        {"$set": {"username": username, "banned": False}},
        upsert=True
    )

async def is_banned(user_id):
    user = await users_db.find_one({"user_id": user_id})
    return user.get("banned", False) if user else False

async def ban_user(user_id):
    await users_db.update_one(
        {"user_id": user_id},
        {"$set": {"banned": True}},
        upsert=True
    )

async def unban_user(user_id):
    await users_db.update_one(
        {"user_id": user_id},
        {"$set": {"banned": False}}
    )

async def get_all_users_count():
    return await users_db.count_documents({})

async def add_admin(user_id):
    await admins_db.update_one(
        {"user_id": user_id},
        {"$set": {"is_admin": True}},
        upsert=True
    )

async def is_admin(user_id, owner_id):
    if user_id == owner_id:
        return True
    admin = await admins_db.find_one({"user_id": user_id})
    return bool(admin)
