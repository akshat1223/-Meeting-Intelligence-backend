from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

class MongoDB:
    client: AsyncIOMotorClient = None
    database = None

mongodb = MongoDB()

async def connect_to_mongodb():
    mongodb.client = AsyncIOMotorClient(settings.MONGO_URL)
    mongodb.database = mongodb.client[settings.DATABASE_NAME]

    await mongodb.client.admin.command('ping')

    print("Connected to MongoDB successfully!")

def get_database():
    return mongodb.database
