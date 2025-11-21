from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from src.models import PostResponse, Posts, Post
from src.core.database import SessionDep
from src.core.auth import AdminDep, is_user, is_admin

router = APIRouter(prefix='/posts', tags=['posts'])

@router.post('/', response_model=PostResponse)
async def create_post(session: SessionDep, post: Post, user: AdminDep):
    post = Posts(text=post.text, author_id=user.id)
    session.add(post)
    await session.commit()
    await session.refresh(post)
    await session.close()
    return post

@router.get('/', dependencies=[Depends(is_user)], response_model=list[PostResponse])
async def show_latest_posts(session: SessionDep, skip: int = 0, limit: int = 10):
    result = await session.execute(
        select(Posts).offset(skip).limit(limit)
        )
    posts = result.scalars().all()
    return posts

@router.get('/today', dependencies=[Depends(is_user)], response_model=PostResponse)
async def read_todays_post(session: SessionDep):
    result = await session.execute(select(Posts).order_by(Posts.id.desc()).limit(1))
    post = result.scalar_one()
    return post

@router.delete('/{post_id}', dependencies=[Depends(is_admin)], status_code=204)
async def delete_post(session: SessionDep, post_id: int):
    result = await session.execute(select(Posts).where(Posts.id == post_id))
    post = result.scalar_one_or_none()
    if post is None:
        raise HTTPException(status_code=404, detail='Post not found')
    await session.delete(post)
    await session.commit()