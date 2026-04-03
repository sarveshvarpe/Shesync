from sqlalchemy.orm import Session
from statistics import mean, stdev
from datetime import timedelta

from app.models.cycle import Cycle
from app.models.cycle_log import CycleLog


def calculate_cycle_lengths(cycles):
    if len(cycles) < 2:
        return []

    lengths = []
    for i in range(1, len(cycles)):
        delta = (cycles[i].start_date - cycles[i - 1].start_date).days
        lengths.append(delta)

    return lengths


def calculate_irregularity_score(lengths):
    if len(lengths) < 2:
        return 0.0

    variability = stdev(lengths)
    avg = mean(lengths)

    if avg == 0:
        return 0.0

    return round(variability / avg, 2)


def calculate_pms_pattern(db: Session, user_id: int):
    logs = db.query(CycleLog).filter(
        CycleLog.user_id == user_id
    ).all()

    if not logs:
        return False

    pms_symptoms = 0
    total_logs = len(logs)

    for log in logs:
        if (
            log.mood in ["irritable", "sad", "anxious"]
            or log.fatigue
            or log.bloating
        ):
            pms_symptoms += 1

    ratio = pms_symptoms / total_logs
    return ratio > 0.4


def calculate_acne_frequency(db: Session, user_id: int):
    logs = db.query(CycleLog).filter(
        CycleLog.user_id == user_id
    ).all()

    if not logs:
        return 0

    acne_days = sum(1 for log in logs if log.acne)
    return round((acne_days / len(logs)) * 100, 2)


def calculate_fatigue_trend(db: Session, user_id: int):
    logs = db.query(CycleLog).filter(
        CycleLog.user_id == user_id
    ).all()

    fatigue_days = sum(1 for log in logs if log.fatigue)

    if not logs:
        return "none"

    ratio = fatigue_days / len(logs)

    if ratio > 0.5:
        return "high"
    elif ratio > 0.25:
        return "moderate"
    else:
        return "low"


def generate_cycle_insights(db: Session, user_id: int):

    cycles = db.query(Cycle).filter(
        Cycle.user_id == user_id,
        Cycle.is_confirmed == True
    ).order_by(Cycle.start_date).all()

    lengths = calculate_cycle_lengths(cycles)

    avg_length = round(mean(lengths), 2) if lengths else 0
    irregular_score = calculate_irregularity_score(lengths)

    return {
        "average_cycle_length": avg_length,
        "cycle_variability_score": irregular_score,
        "pms_pattern_detected": calculate_pms_pattern(db, user_id),
        "acne_frequency_percent": calculate_acne_frequency(db, user_id),
        "fatigue_trend": calculate_fatigue_trend(db, user_id)
    }