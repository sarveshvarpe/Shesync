from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.cycle import Cycle
from app.models.cycle_log import CycleLog
from app.services.health_summary_service import generate_health_summary


router = APIRouter(
    prefix="/health",
    tags=["Health Intelligence"]
)


@router.get("/summary")
def get_health_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cycles = db.query(Cycle).filter(
        Cycle.user_id == current_user.id,
        Cycle.is_confirmed == True
    ).order_by(Cycle.start_date).all()

    logs = db.query(CycleLog).filter(
        CycleLog.user_id == current_user.id
    ).all()

    return generate_health_summary(
        user=current_user,
        cycles=cycles,
        logs=logs
    )