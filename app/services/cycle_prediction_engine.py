from datetime import timedelta


def predict_next_cycle(pattern_data, cycles):

    if not cycles:
        return {
            "next_period_date": None,
            "ovulation_window_start": None,
            "ovulation_window_end": None,
            "prediction_confidence": "low",
            "trend_direction": "insufficient_data"
        }

    last_cycle = cycles[-1]
    avg_length = pattern_data.get("average_cycle_length") or 28
    variability = pattern_data.get("cycle_variability_days") or 0

    # -----------------------------
    # Next Period Prediction
    # -----------------------------
    next_period = last_cycle.start_date + timedelta(days=avg_length)

    # -----------------------------
    # Ovulation Estimate
    # Ovulation ~14 days before next period
    # -----------------------------
    ovulation_day = next_period - timedelta(days=14)
    ovulation_start = ovulation_day - timedelta(days=2)
    ovulation_end = ovulation_day + timedelta(days=2)

    # -----------------------------
    # Trend Direction
    # -----------------------------
    if variability <= 3:
        trend = "stable"
    elif variability <= 7:
        trend = "mild_variation"
    else:
        trend = "high_variation"

    # -----------------------------
    # Confidence Level
    # -----------------------------
    if len(cycles) >= 6 and variability <= 5:
        confidence = "high"
    elif len(cycles) >= 3:
        confidence = "moderate"
    else:
        confidence = "low"

    return {
        "next_period_date": next_period,
        "ovulation_window_start": ovulation_start,
        "ovulation_window_end": ovulation_end,
        "prediction_confidence": confidence,
        "trend_direction": trend
    }