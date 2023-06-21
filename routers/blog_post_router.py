# endpoints for blog post are written here

from fastapi import APIRouter

from models.blog_post_model import BlogPost

router = APIRouter()


@router.get('/posts')
async def get_all_posts():
    return {"Page": "get_all_posts!"}
