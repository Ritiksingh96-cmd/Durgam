"""
Seed script: Creates the default I4C officer account.
Run once: python seed.py
"""
import asyncio
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from datetime import datetime, timezone
from config import settings

# Force UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def seed():
    client = AsyncIOMotorClient(settings.mongodb_url)
    db = client[settings.database_name]

    email = "i4c@gov.in"
    existing = await db.i4c_officers.find_one({"email": email})
    if not existing:
        await db.i4c_officers.insert_one({
            "name": "I4C Officer",
            "email": email,
            "hashed_password": pwd_context.hash("i4c@2024"),
            "role": "i4c",
            "created_at": datetime.now(timezone.utc),
            "is_active": True,
        })
        print("[OK] I4C officer created: i4c@gov.in / i4c@2024")
    else:
        print("[INFO] I4C officer already exists")

    client.close()
    print("Seed complete!")


if __name__ == "__main__":
    asyncio.run(seed())
