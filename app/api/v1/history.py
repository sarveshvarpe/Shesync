from datetime import date
from typing import List

from app.models.user import User
from app.models.cycle import Cycle
from app.models.cycle_log import CycleLog

from app.services.pattern_analyzer import analyze_cycle_patterns
from app.services.risk_engine import calculate_pcos_risk, categorize_risk
from app.services.hormone_index_engine import calculate_hormone_index
from app.services.fertility_engine import calculate_fertility_score
from app.services.health_score_engine import calculate_health_score
from app.services.prediction_engine import generate_cycle_prediction
from app.services.phase_engine import determine_current_phase
from app.services.alert_engine import generate_health_alerts
from app.services.insight_engine import generate_clinical_insight
from app.services.confidence_engine import calculate_data_confidence
from app.services.recommendation_engine import generate_personalized_recommendations
from app.services.trend_engine import analyze_trends
# ======================================================
# PROFILE MODE DETERMINATION
# ======================================================

def determine_profile_mode(age, pattern_data, risk_level):
    if not age:
        return "General Reproductive Intelligence"

    if age <= 18:
        return "Adolescent Cycle Intelligence"
    elif 19 <= age <= 35:
        return "General Reproductive Intelligence"
    elif age > 35:
        return "Advanced Hormonal Monitoring"

    return "General Reproductive Intelligence"


# ======================================================
# MAIN HEALTH SUMMARY ENGINE
# ======================================================

def generate_health_summary(
    user: User,
    cycles: List[Cycle],
    logs: List[CycleLog]
):

    # --------------------------------------------------
    # 1️⃣ Pattern Analysis
    # --------------------------------------------------
    pattern_data = analyze_cycle_patterns(cycles) or {}

    # --------------------------------------------------
    # 2️⃣ Symptom Aggregation
    # --------------------------------------------------
    total_logs = len(logs)

    acne_count = sum(1 for log in logs if getattr(log, "acne", False))
    pms_count = sum(1 for log in logs if getattr(log, "severe_pms", False))
    heavy_bleeding_count = sum(1 for log in logs if getattr(log, "heavy_bleeding", False))
    weight_flag = any(getattr(log, "weight_instability", False) for log in logs)

    symptom_data = {
        "acne_frequency": (acne_count / total_logs * 100) if total_logs else 0,
        "pms_frequency": (pms_count / total_logs * 100) if total_logs else 0,
        "heavy_bleeding_frequency": (heavy_bleeding_count / total_logs * 100) if total_logs else 0,
        "weight_instability": weight_flag
    }

    # --------------------------------------------------
    # 3️⃣ PCOS Risk Engine
    # --------------------------------------------------
    pcos_score = calculate_pcos_risk(pattern_data, symptom_data)
    risk_level = categorize_risk(pcos_score)

    # --------------------------------------------------
    # 4️⃣ Hormone Stability Index
    # --------------------------------------------------
    hormone_index = calculate_hormone_index(pattern_data, symptom_data)

    # --------------------------------------------------
    # 5️⃣ Fertility Score
    # --------------------------------------------------
    fertility_score = calculate_fertility_score(pattern_data)

    # --------------------------------------------------
    # 6️⃣ Health Score
    # --------------------------------------------------
    cycle_health_score = calculate_health_score(
        pattern_data,
        symptom_data,
        pcos_score
    )

    # --------------------------------------------------
    # 7️⃣ Prediction Engine
    # --------------------------------------------------
    prediction_data = generate_cycle_prediction(
        cycles,
        pattern_data
    )

    # --------------------------------------------------
    # 8️⃣ Phase Engine
    # --------------------------------------------------
    phase_data = determine_current_phase(
        cycles,
        pattern_data
    )

    # --------------------------------------------------
    # 9️⃣ Advanced Confidence Engine
    # --------------------------------------------------
    confidence_data = calculate_data_confidence(
        cycles,
        pattern_data,
        logs
    )

    confidence = confidence_data["level"]
    confidence_score = confidence_data["score"]

    # --------------------------------------------------
    # 🔟 Alerts
    # --------------------------------------------------
    alerts = generate_health_alerts(
        pattern_data,
        symptom_data,
        pcos_score,
        cycles
    )

    # --------------------------------------------------
    # 1️⃣1️⃣ Clinical Insights
    # --------------------------------------------------
    insights = generate_clinical_insight(
        pattern_data,
        symptom_data,
        pcos_score,
        risk_level,
        phase_data,
        prediction_data,
        confidence
    )
    recommendations = generate_personalized_recommendations(
    pattern_data,
    symptom_data,
    risk_level,
    phase_data,
    fertility_score,
    confidence)
    trend_analysis = analyze_trends(
    cycles,
    logs,
    pattern_data,
    pcos_score)

    # --------------------------------------------------
    # 1️⃣2️⃣ Profile Mode
    # --------------------------------------------------
    profile_mode = determine_profile_mode(
        getattr(user, "age", None),
        pattern_data,
        risk_level
    )
    create_health_snapshot(db,user,response)

    # --------------------------------------------------
    # FINAL RESPONSE
    # --------------------------------------------------
    return {
        "profile_mode": profile_mode,
        "cycle_health_score": cycle_health_score,
        "hormonal_stability_index": hormone_index,
        "pcos_risk_score": pcos_score,
        "pcos_risk_level": risk_level,
        "fertility_score": fertility_score,
        "confidence": confidence,
        "confidence_score": confidence_score,
        "alerts": alerts,
        "prediction": prediction_data,
        "hormonal_phase": phase_data,
        "insights": insights,
        "recommendations": recommendations,
        "trend_analysis": trend_analysis
    }