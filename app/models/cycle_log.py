from sqlalchemy import (
    Column,
    Integer,
    Date,
    ForeignKey,
    Boolean,
    DateTime,
    Enum,
    Text
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.database import Base


# =========================
# ENUM DEFINITIONS
# =========================

class MoodEnum(str, enum.Enum):
    happy = "happy"
    neutral = "neutral"
    sad = "sad"
    anxious = "anxious"
    irritable = "irritable"


class FlowIntensityEnum(str, enum.Enum):
    none = "none"
    spotting = "spotting"
    light = "light"
    medium = "medium"
    heavy = "heavy"


# =========================
# CYCLE LOG MODEL
# =========================

class CycleLog(Base):
    __tablename__ = "cycle_logs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    cycle_id = Column(Integer, ForeignKey("cycles.id", ondelete="CASCADE"), nullable=False)

    log_date = Column(Date, nullable=False)

    mood = Column(Enum(MoodEnum), nullable=False)
    flow_intensity = Column(Enum(FlowIntensityEnum), default=FlowIntensityEnum.none)

    cramps = Column(Boolean, default=False)
    headache = Column(Boolean, default=False)
    fatigue = Column(Boolean, default=False)
    acne = Column(Boolean, default=False)
    bloating = Column(Boolean, default=False)

    notes = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", backref="cycle_logs")
    cycle = relationship("Cycle", backref="logs")