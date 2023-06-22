from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

# from main import client
from config import Settings

settings = Settings()

# MongoDB connection, get data from .env
username = settings.mongo_username
password = settings.mongo_password

# MongoDB connection setup
connection_string = f"mongodb+srv://{username}:{password}@cluster0.rthfj.mongodb.net/?retryWrites=true&w=majority"
client = AsyncIOMotorClient(connection_string)
db = client["blogging_platform"]


def get_database() -> AsyncIOMotorDatabase:
    return db
