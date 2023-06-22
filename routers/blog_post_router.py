# endpoints for blog post are written here

from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_database

router = APIRouter()


@router.get('/posts')
async def get_posts(db: AsyncIOMotorDatabase = Depends(get_database)):
    """ use get_database to connect to monogo"""

    cursor = db.posts.find()
    posts = await cursor.to_list(length=None)  # Convert cursor to a list

    return {"posts": posts}
