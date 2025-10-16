from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime, timedelta
from fastapi.responses import RedirectResponse
from fastapi_sso.sso.github import GithubSSO

from ..database import SessionLocal
from ..models import User, RefreshSession, RoleEnum
from ..schemas import RegisterIn, LoginIn, TokenPair, RefreshSessionOut, UserOut
from ..security import hash_password, verify_password, make_access_token, make_refresh_token
from ..config import settings
from ..deps import get_db, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

github_sso = GithubSSO(
    client_id=settings.GITHUB_CLIENT_ID,
    client_secret=settings.GITHUB_CLIENT_SECRET,
    redirect_uri=settings.GITHUB_REDIRECT_URL,
)

@router.post("/register", response_model=UserOut)
def register(payload: RegisterIn, db: Session = Depends(get_db)):
    if db.query(User).filter((User.email==payload.email)|(User.username==payload.username)).first():
        raise HTTPException(status_code=409, detail="exists")
    user = User(
        email=payload.email,
        username=payload.username,
        password_hash=hash_password(payload.password),
        role=RoleEnum.user,
        is_author_verified=False
    )
    db.add(user); db.commit(); db.refresh(user)
    return user

@router.post("/login", response_model=TokenPair)
def login(payload: LoginIn, request: Request, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email==payload.email).first()
    if not user or not user.password_hash or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="bad creds")
    jti = uuid4().hex
    refresh = make_refresh_token(user.email, jti)
    sess = RefreshSession(
        user_id=user.id, jti=jti,
        user_agent=request.headers.get("user-agent","unknown"),
        expires_at=datetime.utcnow()+timedelta(days=settings.REFRESH_EXPIRES_DAYS),
    )
    db.add(sess); db.commit()
    return TokenPair(access_token=make_access_token(user.email), refresh_token=refresh)

@router.get("/github/login")
async def github_login():
    return await github_sso.get_login_redirect()

@router.get("/github/callback", response_model=TokenPair)
async def github_callback(request: Request, db: Session = Depends(get_db)):
    user_info = await github_sso.verify_and_process(request)
    email = user_info.email
    username = user_info.display_name or user_info.username or email.split("@")[0]
    user = db.query(User).filter_by(email=email).first()
    if not user:
        user = User(email=email, username=username, role=RoleEnum.user, is_author_verified=False)
        db.add(user); db.commit(); db.refresh(user)
    jti = uuid4().hex
    refresh = make_refresh_token(user.email, jti)
    sess = RefreshSession(
        user_id=user.id, jti=jti,
        user_agent=request.headers.get("user-agent","unknown"),
        expires_at=datetime.utcnow()+timedelta(days=settings.REFRESH_EXPIRES_DAYS),
    )
    db.add(sess); db.commit()
    return TokenPair(access_token=make_access_token(user.email), refresh_token=refresh)

@router.post("/refresh", response_model=TokenPair)
def refresh_token(refresh_token: str, request: Request, db: Session = Depends(get_db)):
    from jose import jwt, JWTError
    from ..config import settings
    try:
        payload = jwt.decode(refresh_token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401)
        email, jti = payload["sub"], payload["jti"]
    except JWTError:
        raise HTTPException(status_code=401)
    sess = db.query(RefreshSession).filter_by(jti=jti, revoked=False).first()
    if not sess or sess.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401)
    # rotate jti
    sess.revoked = True
    new_jti = uuid4().hex
    new_sess = RefreshSession(
        user_id=sess.user_id, jti=new_jti,
        user_agent=request.headers.get("user-agent","unknown"),
        expires_at=datetime.utcnow()+timedelta(days=settings.REFRESH_EXPIRES_DAYS),
    )
    db.add(new_sess); db.commit()
    return TokenPair(access_token=make_access_token(email),
                     refresh_token=make_refresh_token(email, new_jti))

@router.post("/logout")
def logout(refresh_token: str, db: Session = Depends(get_db)):
    from jose import jwt, JWTError
    try:
        payload = jwt.decode(refresh_token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
        jti = payload.get("jti")
    except Exception:
        raise HTTPException(status_code=400)
    sess = db.query(RefreshSession).filter_by(jti=jti).first()
    if sess:
        sess.revoked = True
        db.commit()
    return {"ok": True}

@router.get("/sessions", response_model=list[RefreshSessionOut])
def my_sessions(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    sessions = db.query(RefreshSession).filter_by(user_id=user.id).order_by(RefreshSession.id.desc()).all()
    return sessions
