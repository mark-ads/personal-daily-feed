from fastapi import FastAPI
from enum import Enum
from posts.router import router

app = FastAPI()
app.include_router(router)