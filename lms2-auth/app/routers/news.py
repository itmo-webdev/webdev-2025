from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..deps import get_db, get_current_user, require_roles, resolve_news_and_check_edit
from ..models import User, News, RoleEnum
from ..schemas import NewsIn, NewsOut

router = APIRouter(prefix="/news", tags=["news"])

@router.post("/", response_model=NewsOut)
def create_news(payload: NewsIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.is_author_verified:
        raise HTTPException(status_code=403, detail="not verified author")
    item = News(title=payload.title, body=payload.body, author_id=user.id)
    db.add(item); db.commit(); db.refresh(item)
    return item

@router.put("/{news_id}", response_model=NewsOut)
def update_news(news: News = Depends(resolve_news_and_check_edit),
                payload: NewsIn = None, db: Session = Depends(get_db)):
    news.title, news.body = payload.title, payload.body
    db.commit(); db.refresh(news)
    return news

@router.delete("/{news_id}")
def delete_news(news: News = Depends(resolve_news_and_check_edit), db: Session = Depends(get_db)):
    db.delete(news); db.commit()
    return {"ok": True}
