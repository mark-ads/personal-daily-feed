from fastapi import APIRouter, Depends
from posts.schemas import PostCreate, PostPublic
from deps import get_current_user, CurrentUser

router = APIRouter(prefix='/posts', tags=['posts'])

@router.post('/', dependencies=[Depends(get_current_user)], response_model=PostPublic)
async def create_post(post_in: PostCreate):
    post_in.text = f'{post_in.text} X {post_in.text}'
    return PostCreate(text=post_in.text)

@router.get('/', dependencies=[Depends(get_current_user)], response_model=PostPublic)
async def show_latest_posts(skip: int = 0, limit: int = 10):
    return

@router.get('/today', dependencies=[Depends(get_current_user)], response_model=PostPublic)
async def read_todays_post():
    return {}

@router.delete('/{post_id}', dependencies=[Depends(get_current_user)], response_model=PostPublic)
async def delete_post(post_id: str):
    return {'deleted': 'post_id'}