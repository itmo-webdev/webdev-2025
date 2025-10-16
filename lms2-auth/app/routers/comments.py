from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..deps import get_db, get_current_user, resolve_comment_and_check_edit
from ..models import User, Comment
from ..schemas import CommentIn, CommentOut

router = APIRouter(prefix="/comments", tags=["comments"])

@router.post("/{news_id}", response_model=CommentOut)
def create_comment(news_id: int, payload: CommentIn,
                   user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    c = Comment(body=payload.body, news_id=news_id, author_id=user.id)
    db.add(c); db.commit(); db.refresh(c)
    return c

@router.put("/{comment_id}", response_model=CommentOut)
def update_comment(cmt: Comment = Depends(resolve_comment_and_check_edit),
                   payload: CommentIn = None, db: Session = Depends(get_db)):
    cmt.body = payload.body
    db.commit(); db.refresh(cmt)
    return cmt

@router.delete("/{comment_id}")
def delete_comment(cmt: Comment = Depends(resolve_comment_and_check_edit), db: Session = Depends(get_db)):
    db.delete(cmt); db.commit()
    return {"ok": True}
