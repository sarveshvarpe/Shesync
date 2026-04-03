from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
    Text,
    Enum,
    String
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.database import Base


# =========================
# ENUM FOR MESSAGE ROLE
# =========================

class MessageRole(str, enum.Enum):
    user = "user"
    assistant = "assistant"


# =========================
# CHAT SESSION MODEL
# =========================

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    title = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", backref="chat_sessions")
    messages = relationship("ChatMessage", backref="session", cascade="all, delete")


# =========================
# CHAT MESSAGE MODEL
# =========================

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(Integer, ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False)

    role = Column(Enum(MessageRole), nullable=False)
    content = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())