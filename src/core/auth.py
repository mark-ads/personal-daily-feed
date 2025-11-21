from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from src.core.database import SessionDep
from src.models import UserCreate, Users, User
from datetime import datetime, timedelta
from jose import JWTError, jwt
from src.core.config import settings
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from src.core.security import verify_password

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 15
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/users/login')

async def authenticate_user(username: str, password: str, session: AsyncSession) -> Users:
    result = await session.execute(select(Users).where(Users.username == username))
    user = result.scalar_one_or_none()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

def create_access_token(data: dict) -> dict:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt

async def is_user(session: SessionDep, token: str = Depends(oauth2_scheme)) -> Users:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        if username is None:
            raise HTTPException(status_code=401, detail='Invalid token')
    except JWTError:
        raise HTTPException(status_code=401, detail='Invalid token')

    result = await session.execute(select(Users).where(Users.username == username))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=401, detail='User not found')
    return user

IsUserDep = Annotated[User, Depends(is_user)]

async def is_admin(session: SessionDep, user: IsUserDep) -> Users:
    if user.superuser is False:
        raise HTTPException(status_code=403, detail='User is not admin')
    return user

AdminDep = Annotated[bool, Depends(is_admin)]