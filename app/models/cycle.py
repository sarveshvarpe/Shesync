from sqlalchemy import Column, Integer, Date, ForeignKey, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Cycle(Base):
    __tablename__ = "cycles"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)

    is_confirmed = Column(Boolean, default=False)
    is_irregular = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", backref="cycles")