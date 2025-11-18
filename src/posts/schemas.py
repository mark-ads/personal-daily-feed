from pydantic import BaseModel
from src.utils import set_current_date

class PostBase(BaseModel):
    text : str


class PostCreate(PostBase):
    pass


class PostPublic(PostBase):
    id: str | None = 'id'
    created_at : str = set_current_date()
