from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.cycle import Cycle
from app.models.cycle_log import CycleLog

from app.services.health_summary_service import generate_health_summary
from app.services.report_service import generate_health_report


router = APIRouter(prefix="/report", tags=["Report"])


@router.get("/download")
def download_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    cycles = db.query(Cycle).filter(
        Cycle.user_id == current_user.id
    ).all()

    logs = db.query(CycleLog).filter(
        CycleLog.user_id == current_user.id
    ).all()

    summary = generate_health_summary(
        current_user,
        cycles,
        logs
    )

    pdf_buffer = generate_health_report(
        db,
        current_user,
        summary
    )

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=shesync-report.pdf"
        }
    )