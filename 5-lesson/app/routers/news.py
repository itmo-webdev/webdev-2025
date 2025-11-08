# app/routers/news.py
from fastapi import APIRouter
from app.tasks.email_tasks import send_news_email

router = APIRouter(prefix="/news", tags=["news"])

@router.post("")
def create_news(title: str):
    # Demo: news_id giả lập; khi có DB thì lấy new.id sau khi insert
    news_id = 123
    users = ["user1@example.com", "user2@example.com"]

    for email in users:
        send_news_email.delay(email, news_id, title)

    return {"ok": True, "queued_for": len(users)}
