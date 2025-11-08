# app/tasks/email_tasks.py
from datetime import datetime, timedelta
from typing import Sequence
import os, json, redis
from pathlib import Path
import logging

from app.celery_app import celery

LOG_PATH = Path(os.getenv("EMAIL_LOG_FILE", "email_worker.log")).resolve()

logger = logging.getLogger("email_worker")      
logger.setLevel(logging.INFO)
if not logger.handlers:                        
    fh = logging.FileHandler(LOG_PATH, encoding="utf-8")
    fh.setLevel(logging.INFO)
    fh.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(fh)
logger.propagate = False                        

def log(line: str) -> None:
    logger.info(f"[{datetime.now().isoformat()}] {line}")

r = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))

@celery.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,          
    retry_jitter=True,
    retry_kwargs={"max_retries": 5},
)
def send_news_email(self, user_email: str, news_id: int, news_title: str) -> str:
    key = f"sent:news:{news_id}"
    if r.sadd(key, user_email) == 0:
        log(f"SKIP already-sent news={news_id} to {user_email}")
        return "skipped"

    log(f"SEND news={news_id} to {user_email} :: title='{news_title}'")
    return "ok"

@celery.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_jitter=True,
    retry_kwargs={"max_retries": 5},
)
def send_weekly_digest(self) -> str:
    last_week = (datetime.utcnow() - timedelta(days=7)).isoformat()
    digest = {
        "since": last_week,
        "items": [
            {"id": 101, "title": "Новая функция A"},
            {"id": 102, "title": "Анонс релиза 1.2"},
        ],
    }
    users: Sequence[str] = ["user1@example.com", "user2@example.com"]
    for email in users:
        log(f"DIGEST -> {email} :: {json.dumps(digest, ensure_ascii=False)}")
    return "ok"