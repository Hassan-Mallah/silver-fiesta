# endpoints for blog post are written here

from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.database import get_database
from models.blog_post_model import BlogPost

router = APIRouter()


@router.get('/posts')
async def get_posts(db: AsyncIOMotorDatabase = Depends(get_database)):
    """ use get_database to connect to mongo """

    posts = []
    async for post in db.posts.find():
        # Convert ObjectId to string
        post["_id"] = str(post["_id"])

        posts.append(post)

    return posts


@router.post('/create_post')
async def create_post(post: BlogPost, db: AsyncIOMotorDatabase = Depends(get_database)):
    """ get data and save it to mongo """"

    data = post.dict()

    result = await db.posts.insert_one(data)
    return {"message": "Post created", "post_id": str(result.inserted_id)}
