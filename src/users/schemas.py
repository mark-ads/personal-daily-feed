from pydantic import BaseModel, Field

class UserBase(BaseModel):
    login: str = Field(default='Mark', max_length=255)


class UserCreate(UserBase):
    pass


class UserPublic(UserBase):
    authorized: bool = True


class User(UserBase):
    login: str = 'Max'