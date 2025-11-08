# app/main.py
from fastapi import FastAPI
from app.routers.news import router as news_router

app = FastAPI(title="WebDev-2025 Lesson 5 - Email Worker Demo")

@app.get("/health")
def health():
    return {"status": "ok"}

# mount router
app.include_router(news_router)