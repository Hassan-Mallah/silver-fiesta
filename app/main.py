import uvicorn
from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, workers=3)
