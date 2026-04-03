from pydantic import BaseModel
from datetime import date
from typing import Optional
from enum import Enum


class MoodEnum(str, Enum):
    happy = "happy"
    neutral = "neutral"
    sad = "sad"
    anxious = "anxious"
    irritable = "irritable"


class FlowIntensityEnum(str, Enum):
    none = "none"
    spotting = "spotting"
    light = "light"
    medium = "medium"
    heavy = "heavy"


class CycleLogCreate(BaseModel):
    cycle_id: int
    log_date: date
    mood: MoodEnum
    flow_intensity: FlowIntensityEnum = FlowIntensityEnum.none
    cramps: bool = False
    headache: bool = False
    fatigue: bool = False
    acne: bool = False
    bloating: bool = False
    notes: Optional[str] = None


class CycleLogResponse(BaseModel):
    id: int
    cycle_id: int
    log_date: date
    mood: MoodEnum
    flow_intensity: FlowIntensityEnum
    cramps: bool
    headache: bool
    fatigue: bool
    acne: bool
    bloating: bool
    notes: Optional[str]

    class Config:
        from_attributes = True