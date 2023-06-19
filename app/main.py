import uvicorn
from fastapi import FastAPI, Request
from motor.motor_asyncio import AsyncIOMotorClient

from config import Settings

app = FastAPI()
settings = Settings()

# MongoDB connection, get data from .env
username = settings.mongo_username
password = settings.mongo_password

connection_string = f"mongodb+srv://{username}:{password}@cluster0.rthfj.mongodb.net/?retryWrites=true&w=majority"
client = AsyncIOMotorClient(connection_string)


@app.get("/")
async def read_root():
    return {"Hello": "World!"}


@app.get("/ping")
async def ping_mongo():
    # Send a ping to confirm a successful connection

    try:
        ping = await client.admin.command('ping')

        result = {
            'ping': ping,
            'message': 'Pinged your deployment. You successfully connected to MongoDB!'

        }
        return {"result": result}
    except Exception as e:
        return {"error": e}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, workers=3)
