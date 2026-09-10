from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

client = None
db = None

async def connect_to_mongodb():
    global client, db
    client = AsyncIOMotorClient(settings.mongodb_url)
    db = client[settings.database_name]
    # Create indexes
    await db.users.create_index("email", unique=True)
    await db.banks.create_index("email", unique=True)
    await db.complaints.create_index("complaint_no", unique=True)
    await db.notifications.create_index([("account_no", 1), ("bank_ifsc_prefix", 1)])
    print(f"[OK] Connected to MongoDB: {settings.database_name}")


async def close_mongodb_connection():
    global client
    if client:
        client.close()
        print("[INFO] Disconnected from MongoDB")


def get_database():
    return db
