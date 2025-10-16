from fastapi import FastAPI
from .routers import auth, news, comments

app = FastAPI(title="LMS 2.0 Auth")

app.include_router(auth.router)
app.include_router(news.router)
app.include_router(comments.router)
