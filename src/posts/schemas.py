from pydantic import BaseModel
from utils import set_current_date

class PostBase(BaseModel):
    text : str


class PostCreate(PostBase):
    created_at : str = set_current_date()