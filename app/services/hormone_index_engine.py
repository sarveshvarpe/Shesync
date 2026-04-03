def calculate_hormone_index(pattern_data, symptom_data):
    """
    Returns Hormonal Stability Index (0–100)
    Higher = more stable hormonal patterns
    """

    score = 100

    variability = pattern_data.get("cycle_variability_days") or 0
    irregular = pattern_data.get("irregular", False)

    acne = symptom_data.get("acne_frequency") or 0
    pms = symptom_data.get("pms_frequency") or 0
    heavy = symptom_data.get("heavy_bleeding_frequency") or 0
    weight_flag = symptom_data.get("weight_instability", False)

    # -----------------------------
    # 1️⃣ Cycle Variability Penalty (max 30)
    # -----------------------------
    variability_penalty = min(variability * 2, 30)

    if irregular:
        variability_penalty += 5

    variability_penalty = min(variability_penalty, 30)

    # -----------------------------
    # 2️⃣ Acne Penalty (max 20)
    # -----------------------------
    acne_penalty = min(acne * 0.2, 20)

    # -----------------------------
    # 3️⃣ PMS Penalty (max 20)
    # -----------------------------
    pms_penalty = min(pms * 0.2, 20)

    # -----------------------------
    # 4️⃣ Heavy Bleeding Penalty (max 15)
    # -----------------------------
    heavy_penalty = min(heavy * 0.15, 15)

    # -----------------------------
    # 5️⃣ Weight Instability Penalty (15 fixed)
    # -----------------------------
    weight_penalty = 15 if weight_flag else 0

    total_penalty = (
        variability_penalty +
        acne_penalty +
        pms_penalty +
        heavy_penalty +
        weight_penalty
    )

    final_score = max(0, round(score - total_penalty))

    return final_score