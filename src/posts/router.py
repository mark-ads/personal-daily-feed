from fastapi import APIRouter
from posts.schemas import PostCreate

router = APIRouter(prefix='/posts', tags=['posts'])

@router.post('/')
async def create_post(post_in: PostCreate):
    return post_in

@router.get('/')
async def show_latest_posts(skip: int = 0, limit: int = 10):
    return

@router.get('/today')
async def read_todays_post():
    return {}