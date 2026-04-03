from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    refresh_token = Column(String, nullable=False)

    device_type = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())