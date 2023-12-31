# endpoints for blog post are written here

from bson import ObjectId

from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.cursor import Cursor

from app.database import get_database
from models.blog_post_model import BlogPost

router = APIRouter()


@router.get('/posts/{post_id}')
async def get_post(post_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    """ using post_id get a post """

    # try to create ObjectId and get post
    try:
        post = await db.posts.find_one({'_id': ObjectId(post_id)})
    except:
        return HTTPException(status_code=400, detail='Incorrect post_id')

    if not post:
        return HTTPException(status_code=400, detail='Post not found')

    post['_id'] = str(post['_id'])
    return post


@router.delete('/posts/{post_id}')
async def delete_post(post_id: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    """ using post_id delete a post """

    try:
        result = await db.posts.delete_one({'_id': ObjectId(post_id)})
    except:
        return HTTPException(status_code=400, detail='Incorrect post_id')

    # check if delete was successful
    if result.deleted_count == 0:
        return HTTPException(status_code=400, detail='Post not found')

    return {'message': 'Post deleted'}


@router.get('/posts_page')
async def get_posts_page(page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100),
                         db: AsyncIOMotorDatabase = Depends(get_database)):
    """ get posts using pagination """

    # Calculate the number of records to skip based on page number
    skip = (page - 1) * limit

    # get the page records
    cursor: Cursor = db.posts.find().skip(skip).limit(limit)
    posts = [BlogPost(**{**post, "_id": str(post["_id"])}) async for post in cursor]

    # get the total count of records
    total_count = await db.posts.count_documents({})

    # Create a response payload with pagination metadata
    response = {
        "page": page,
        "limit": limit,
        "total_count": total_count,
        "data": posts,
    }

    return response

@router.get('/posts')
async def get_posts(db: AsyncIOMotorDatabase = Depends(get_database)):
    """ use get_database to connect to mongo """

    posts = []
    async for post in db.posts.find():
        # Convert ObjectId to string
        post['_id'] = str(post['_id'])

        posts.append(post)

    return posts


@router.post('/create_post')
async def create_post(post: BlogPost, db: AsyncIOMotorDatabase = Depends(get_database)):
    """ get data and save it to mongo """

    data = post.dict()

    result = await db.posts.insert_one(data)
    return {'message': 'Post created', 'post_id': str(result.inserted_id)}


@router.put('/update_post')
async def update_post(post_id: str, post_update: BlogPost, db: AsyncIOMotorDatabase = Depends(get_database)):
    """ using put request, update a post """

    # set: update these fields
    # exclude_unset: dont update missing fields
    updated_post = await db.posts.find_one_and_update(
        {'_id': ObjectId(post_id)},
        {'$set': post_update.dict(exclude_unset=True)},
        return_document=True
    )

    updated_post['_id'] = str(updated_post['_id'])
    return updated_post
