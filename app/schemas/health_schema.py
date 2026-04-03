from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class AlertItem(BaseModel):
    type: str
    severity: str
    message: str


class PredictionData(BaseModel):
    next_period_date: Optional[date]
    ovulation_window_start: Optional[date]
    ovulation_window_end: Optional[date]
    prediction_confidence: str
    trend_direction: str


class HormonalPhase(BaseModel):
    current_phase: str
    phase_day: Optional[int]
    phase_stability: str


class HealthSummaryResponse(BaseModel):
    profile_mode: str
    cycle_health_score: int
    hormonal_stability_index: int
    pcos_risk_score: float
    pcos_risk_level: str
    fertility_score: int
    confidence: str
    alerts: List[AlertItem]
    prediction: PredictionData
    hormonal_phase: HormonalPhase
    insights: List[str]
    recommendations: List[str]
    trend_analysis: dict