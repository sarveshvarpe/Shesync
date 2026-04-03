from datetime import date


def calculate_data_confidence(cycles, pattern_data, logs):
    """
    Returns:
    {
        "score": int (0–100),
        "level": "low" | "moderate" | "high"
    }
    """

    score = 0

    # ---------------------------------
    # 1️⃣ Cycle Count Weight (40 max)
    # ---------------------------------
    cycle_count = len(cycles)

    if cycle_count >= 8:
        score += 40
    elif cycle_count >= 5:
        score += 30
    elif cycle_count >= 3:
        score += 20
    elif cycle_count >= 1:
        score += 10

    # ---------------------------------
    # 2️⃣ Variability Stability (20 max)
    # ---------------------------------
    variability = pattern_data.get("cycle_variability_days") or 0

    if variability <= 2:
        score += 20
    elif variability <= 5:
        score += 15
    elif variability <= 8:
        score += 10
    else:
        score += 5

    # ---------------------------------
    # 3️⃣ Irregularity Penalty (-10)
    # ---------------------------------
    if pattern_data.get("irregular"):
        score -= 10

    # ---------------------------------
    # 4️⃣ Log Consistency (20 max)
    # ---------------------------------
    if logs:
        log_ratio = len(logs) / max(cycle_count, 1)

        if log_ratio >= 5:
            score += 20
        elif log_ratio >= 3:
            score += 15
        elif log_ratio >= 1:
            score += 10

    # ---------------------------------
    # 5️⃣ Recency Weight (20 max)
    # ---------------------------------
    if cycles:
        last_cycle = cycles[-1]
        days_since_last = (date.today() - last_cycle.start_date).days

        if days_since_last <= 35:
            score += 20
        elif days_since_last <= 60:
            score += 10
        else:
            score += 5

    # ---------------------------------
    # Normalize Score
    # ---------------------------------
    score = max(0, min(100, score))

    if score >= 70:
        level = "high"
    elif score >= 40:
        level = "moderate"
    else:
        level = "low"

    return {
        "score": score,
        "level": level
    }