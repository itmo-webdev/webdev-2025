import enum
from datetime import datetime, timedelta
from sqlalchemy import (Column, Integer, String, Text, Boolean, Enum,
                        DateTime, ForeignKey, UniqueConstraint)
from sqlalchemy.orm import relationship
from .database import Base

class RoleEnum(str, enum.Enum):
    user = "user"
    admin = "admin"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=True)  # None cho OAuth-only
    role = Column(Enum(RoleEnum), default=RoleEnum.user, nullable=False)
    is_author_verified = Column(Boolean, default=False, nullable=False)

    news = relationship("News", back_populates="author")
    comments = relationship("Comment", back_populates="author")

class RefreshSession(Base):
    __tablename__ = "refresh_sessions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    jti = Column(String(64), unique=True, nullable=False)
    user_agent = Column(Text, nullable=False)  # yêu cầu lưu user-agent
    expires_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, default=False, nullable=False)
    user = relationship("User")

class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    body = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    author = relationship("User", back_populates="news")

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    body = Column(Text, nullable=False)
    news_id = Column(Integer, ForeignKey("news.id", ondelete="CASCADE"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    author = relationship("User", back_populates="comments")
    news = relationship("News")
    __table_args__ = (UniqueConstraint('id', 'news_id', name='uq_comment_news'),)
