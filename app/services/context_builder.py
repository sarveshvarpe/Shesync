from sqlalchemy.orm import Session
from datetime import datetime

from app.services.insight_service import generate_cycle_insights
from app.models.cycle_log import CycleLog


def build_user_health_context(db: Session, user_id: int) -> str:
    """
    Build structured health summary for LLM.
    This ensures the model receives summarized, clean context.
    """

    insights = generate_cycle_insights(db, user_id)

    recent_logs = (
        db.query(CycleLog)
        .filter(CycleLog.user_id == user_id)
        .order_by(CycleLog.log_date.desc())
        .limit(7)
        .all()
    )

    log_summary = []

    for log in recent_logs:
        log_summary.append(
            f"Date: {log.log_date}, "
            f"Mood: {log.mood}, "
            f"Flow: {log.flow_intensity}, "
            f"Cramps: {log.cramps}, "
            f"Fatigue: {log.fatigue}, "
            f"Acne: {log.acne}, "
            f"Bloating: {log.bloating}"
        )

    formatted_logs = "\n".join(log_summary) if log_summary else "No recent logs."

    context = f"""
User Health Summary:
- Average Cycle Length: {insights['average_cycle_length']} days
- Cycle Variability Score: {insights['cycle_variability_score']}
- PMS Pattern Detected: {insights['pms_pattern_detected']}
- Acne Frequency: {insights['acne_frequency_percent']}%
- Fatigue Trend: {insights['fatigue_trend']}

Recent 7-Day Logs:
{formatted_logs}

Important:
- Provide suggestions only.
- Do NOT diagnose medical conditions.
- Do NOT claim the user has PCOS or any disease.
- Encourage consulting a healthcare professional when appropriate.
"""

    return context.strip()