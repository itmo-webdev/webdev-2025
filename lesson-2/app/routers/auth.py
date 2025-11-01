from fastapi import APIRouter, HTTPException, Request, Depends, Form
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.services.session_service import create_session, get_session, delete_session
from app.services.user_cache import get_user_public
from app.database import get_db
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
async def login(username: str = Form(...), password: str = Form(...), db: AsyncSession = Depends(get_db)):
    # TODO: thay bằng xác thực thực tế
    row = (await db.execute(text("SELECT id, username, role, is_active FROM users WHERE username=:u"),
                            {"u": username})).mappings().first()
    if not row or password != "password":  # demo
        raise HTTPException(status_code=401, detail="Invalid creds")
    sid = await create_session(row["id"], row["role"])
    resp = JSONResponse({"session_id": sid, "user_id": row["id"], "role": row["role"]})
    resp.set_cookie("session_id", sid, max_age=settings.REFRESH_TTL_SECONDS, httponly=True, samesite="lax")
    return resp

@router.post("/logout")
async def logout(request: Request):
    sid = request.cookies.get("session_id") or request.headers.get("X-Session-Id")
    if sid: await delete_session(sid)
    return {"ok": True}

async def current_user(request: Request, db: AsyncSession = Depends(get_db)):
    sid = request.cookies.get("session_id") or request.headers.get("X-Session-Id")
    if not sid: raise HTTPException(401, "Missing session")
    s = await get_session(sid)
    if not s: raise HTTPException(401, "Invalid session")
    user = await get_user_public(s["user_id"], db)
    if not user: raise HTTPException(401, "User not found/disabled")
    return user

@router.get("/me")
async def me(user = Depends(current_user)):
    return user