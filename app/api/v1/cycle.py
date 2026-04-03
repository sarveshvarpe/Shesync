from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
from app.core.dependencies import get_db, get_current_user
from app.models.cycle import Cycle
from app.models.user import User
from app.schemas.cycle_schema import (
    StartCycleRequest,
    EndCycleRequest,
    CycleResponse
)

router = APIRouter(prefix="/cycle", tags=["Cycle"])


# =========================
# START CYCLE
# =========================
@router.post("/start", response_model=CycleResponse)
def start_cycle(
    payload: StartCycleRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if there is already an active cycle
    active_cycle = db.query(Cycle).filter(
        Cycle.user_id == current_user.id,
        Cycle.is_confirmed == False
    ).first()

    if active_cycle:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There is already an active cycle. End it first."
        )

    cycle = Cycle(
        user_id=current_user.id,
        start_date=payload.start_date,
        is_confirmed=False
    )

    db.add(cycle)
    db.commit()
    db.refresh(cycle)

    return cycle


# =========================
# END CYCLE
# =========================
@router.post("/end", response_model=CycleResponse)
def end_cycle(
    payload: EndCycleRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cycle = db.query(Cycle).filter(
        Cycle.user_id == current_user.id,
        Cycle.is_confirmed == False
    ).order_by(Cycle.start_date.desc()).first()

    if not cycle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active cycle found"
        )

    if payload.end_date < cycle.start_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End date cannot be before start date"
        )

    cycle.end_date = payload.end_date
    cycle.is_confirmed = True

    db.commit()
    db.refresh(cycle)

    return cycle


# =========================
# GET CYCLE HISTORY
# =========================
@router.get("/history", response_model=list[CycleResponse])
def get_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cycles = db.query(Cycle).filter(
        Cycle.user_id == current_user.id
    ).order_by(Cycle.start_date.desc()).all()

    return cycles

#==========================
#predict 
#==========================
from datetime import timedelta
from statistics import mean
from fastapi import HTTPException

@router.get("/predict")
def predict_cycle(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cycles = db.query(Cycle).filter(
        Cycle.user_id == current_user.id,
        Cycle.is_confirmed == True
    ).order_by(Cycle.start_date).all()

    if len(cycles) < 2:
        raise HTTPException(
            status_code=400,
            detail="At least 2 completed cycles required for prediction"
        )

    # Calculate cycle lengths
    cycle_lengths = []
    for i in range(1, len(cycles)):
        diff = (cycles[i].start_date - cycles[i-1].start_date).days
        cycle_lengths.append(diff)

    avg_cycle_length = int(mean(cycle_lengths))

    last_cycle = cycles[-1]

    next_period_date = last_cycle.start_date + timedelta(days=avg_cycle_length)

    ovulation_date = next_period_date - timedelta(days=14)

    fertile_start = ovulation_date - timedelta(days=5)
    fertile_end = ovulation_date

    return {
        "average_cycle_length": avg_cycle_length,
        "next_period_date": next_period_date,
        "ovulation_date": ovulation_date,
        "fertile_window_start": fertile_start,
        "fertile_window_end": fertile_end,
        "irregular": False  # We will calculate this later
    }
from app.services.insight_service import generate_cycle_insights


@router.get("/insights")
def get_cycle_insights(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return generate_cycle_insights(db, current_user.id)