from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from jose import JWTError
from .database import SessionLocal
from .models import User, RoleEnum, News, Comment, RefreshSession
from .security import decode_token

bearer = HTTPBearer(auto_error=False)

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer),
                     db: Session = Depends(get_db)) -> User:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        payload = decode_token(credentials.credentials)
        if payload.get("type") != "access":
            raise HTTPException(status_code=401)
        email = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user = db.query(User).filter_by(email=email).first()
    if not user:
        raise HTTPException(status_code=401)
    return user

def require_roles(*roles: RoleEnum):
    def _inner(user: User = Depends(get_current_user)):
        if roles and user.role not in roles:
            raise HTTPException(status_code=403, detail="insufficient role")
        return user
    return _inner

def resolve_news_and_check_edit(news_id: int,
                                user: User = Depends(get_current_user),
                                db: Session = Depends(get_db)) -> News:
    news = db.query(News).get(news_id)
    if not news:
        raise HTTPException(status_code=404, detail="news not found")
    if user.role != RoleEnum.admin and news.author_id != user.id:
        raise HTTPException(status_code=403, detail="not owner/admin")
    return news

def resolve_comment_and_check_edit(comment_id: int,
                                   user: User = Depends(get_current_user),
                                   db: Session = Depends(get_db)) -> Comment:
    cmt = db.query(Comment).get(comment_id)
    if not cmt:
        raise HTTPException(status_code=404)
    if user.role != RoleEnum.admin and cmt.author_id != user.id:
        raise HTTPException(status_code=403)
    return cmt
