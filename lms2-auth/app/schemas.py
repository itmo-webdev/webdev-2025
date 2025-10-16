from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)  
    id: int
    email: EmailStr
    username: str
    role: str
    is_author_verified: bool

class RegisterIn(BaseModel):
    email: EmailStr
    username: str
    password: str

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshSessionOut(BaseModel):
    id: int
    jti: str
    user_agent: str
    expires_at: datetime
    revoked: bool
    class Config: orm_mode = True

class NewsIn(BaseModel):
    title: str
    body: str

class NewsOut(BaseModel):
    id: int
    title: str
    body: str
    author_id: int
    class Config: orm_mode = True

class CommentIn(BaseModel):
    body: str

class CommentOut(BaseModel):
    id: int
    body: str
    news_id: int
    author_id: int
    class Config: orm_mode = True
