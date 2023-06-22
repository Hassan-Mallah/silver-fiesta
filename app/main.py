import uvicorn
from fastapi import FastAPI, Request
from database import client

from routers.blog_post_router import router

app = FastAPI()
app.include_router(router)


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
