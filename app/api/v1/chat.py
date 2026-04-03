from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.services.chat_service import generate_ai_response


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


# =========================
# Request Schema
# =========================
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[int] = None


# =========================
# Response Schema
# =========================
from typing import List


class RiskSummary(BaseModel):
    pcos_risk_score: float
    risk_level: str


class Alert(BaseModel):
    type: str
    severity: str
    message: str


class ChatResponse(BaseModel):
    session_id: int
    reply: str
    confidence: str
    health_score: int
    medical_flag: bool
    risk_summary: RiskSummary
    alerts: List[Alert]

# =========================
# Chat Endpoint
# =========================
@router.post("/", response_model=ChatResponse)
def chat_with_ai(
    payload: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not payload.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    return generate_ai_response(
    db=db,
    user=current_user,
    message=payload.message,
    session_id=payload.session_id)