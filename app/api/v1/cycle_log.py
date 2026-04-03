from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date

from app.core.dependencies import get_db, get_current_user
from app.models.cycle_log import CycleLog
from app.models.cycle import Cycle
from app.models.user import User
from app.schemas.cycle_log_schema import (
    CycleLogCreate,
    CycleLogResponse
)

router = APIRouter(prefix="/cycle", tags=["Cycle Logs"])


# =========================
# CREATE OR UPDATE DAILY LOG
# =========================
@router.post("/log", response_model=CycleLogResponse)
def create_or_update_log(
    payload: CycleLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Ensure cycle belongs to user
    cycle = db.query(Cycle).filter(
        Cycle.id == payload.cycle_id,
        Cycle.user_id == current_user.id
    ).first()

    if not cycle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cycle not found for this user"
        )

    # Check if log already exists for that date
    existing_log = db.query(CycleLog).filter(
        CycleLog.user_id == current_user.id,
        CycleLog.log_date == payload.log_date
    ).first()

    if existing_log:
        # Update existing
        existing_log.mood = payload.mood
        existing_log.flow_intensity = payload.flow_intensity
        existing_log.cramps = payload.cramps
        existing_log.headache = payload.headache
        existing_log.fatigue = payload.fatigue
        existing_log.acne = payload.acne
        existing_log.bloating = payload.bloating
        existing_log.notes = payload.notes

        db.commit()
        db.refresh(existing_log)
        return existing_log

    # Create new log
    new_log = CycleLog(
        user_id=current_user.id,
        cycle_id=payload.cycle_id,
        log_date=payload.log_date,
        mood=payload.mood,
        flow_intensity=payload.flow_intensity,
        cramps=payload.cramps,
        headache=payload.headache,
        fatigue=payload.fatigue,
        acne=payload.acne,
        bloating=payload.bloating,
        notes=payload.notes
    )

    db.add(new_log)
    db.commit()
    db.refresh(new_log)

    return new_log


# =========================
# GET ALL LOGS FOR USER
# =========================
@router.get("/logs", response_model=list[CycleLogResponse])
def get_user_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    logs = db.query(CycleLog).filter(
        CycleLog.user_id == current_user.id
    ).order_by(CycleLog.log_date.desc()).all()

    return logs