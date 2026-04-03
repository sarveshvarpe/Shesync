def calculate_fertility_score(pattern_data: dict) -> int:
    """
    Fertility Stability Score (0–100)

    Higher score = More predictable ovulation patterns
    Lower score = Higher variability / irregularity

    Safe for incomplete data.
    """

    # ----------------------------------
    # 0️⃣ Safe Extraction
    # ----------------------------------

    avg_length = pattern_data.get("average_cycle_length") or 0
    variability = pattern_data.get("cycle_variability_days") or 0
    irregular = pattern_data.get("irregular") or False

    # Ensure numeric safety
    try:
        avg_length = float(avg_length)
    except (TypeError, ValueError):
        avg_length = 0

    try:
        variability = float(variability)
    except (TypeError, ValueError):
        variability = 0

    score = 100

    # ----------------------------------
    # 1️⃣ Regularity Penalty (Max 40)
    # ----------------------------------

    regularity_penalty = 40 if irregular else 0

    # ----------------------------------
    # 2️⃣ Variability Penalty (Max 30)
    # ----------------------------------

    # Each day of variability reduces predictability
    variability_penalty = min(variability * 2, 30)

    # ----------------------------------
    # 3️⃣ Average Length Penalty (Max 30)
    # Ideal cycle range: 21–35 days
    # ----------------------------------

    length_penalty = 0

    if avg_length > 0:
        if avg_length < 21:
            length_penalty = min((21 - avg_length) * 2, 30)
        elif avg_length > 35:
            length_penalty = min((avg_length - 35) * 2, 30)

    # ----------------------------------
    # 4️⃣ Low Data Stability Adjustment
    # ----------------------------------

    # If insufficient cycle data (avg_length == 0),
    # slightly reduce score confidence
    if avg_length == 0:
        score -= 15

    # ----------------------------------
    # 5️⃣ Final Score Calculation
    # ----------------------------------

    total_penalty = (
        regularity_penalty +
        variability_penalty +
        length_penalty
    )

    final_score = max(0, min(100, round(score - total_penalty)))

    return final_score