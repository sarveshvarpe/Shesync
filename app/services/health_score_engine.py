def calculate_health_score(pattern_data, symptom_data, pcos_score):
    """
    Returns health score from 0 to 100
    Higher = better menstrual stability
    """

    score = 100

    # -----------------------------
    # 1️⃣ Cycle Stability Penalty (max 40)
    # -----------------------------

    variability = pattern_data.get("cycle_variability_days") or 0
    avg_length = pattern_data.get("average_cycle_length") or 0
    irregular = pattern_data.get("irregular", False)

    cycle_penalty = 0

    if variability:
        cycle_penalty += min(variability * 2, 20)

    if avg_length and avg_length > 40:
        cycle_penalty += min((avg_length - 40) * 1.5, 10)

    if irregular:
        cycle_penalty += 10

    cycle_penalty = min(cycle_penalty, 40)

    # -----------------------------
    # 2️⃣ Symptom Burden Penalty (max 30)
    # -----------------------------

    acne = symptom_data.get("acne_frequency", 0)
    pms = symptom_data.get("pms_frequency", 0)
    heavy = symptom_data.get("heavy_bleeding_frequency", 0)

    symptom_penalty = (
        acne * 0.1 +
        pms * 0.1 +
        heavy * 0.1
    )

    symptom_penalty = min(symptom_penalty, 30)

    # -----------------------------
    # 3️⃣ Risk Penalty (max 30)
    # -----------------------------

    risk_penalty = pcos_score * 30

    # -----------------------------
    # Final Score
    # -----------------------------

    total_penalty = cycle_penalty + symptom_penalty + risk_penalty

    final_score = max(0, round(score - total_penalty))

    return final_score