from datetime import timedelta, date


def generate_cycle_prediction(cycles, pattern_data):
    """
    Predicts next period and ovulation window.
    """

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

    # Predict next period
    next_period = last_cycle.start_date + timedelta(days=int(avg_length))

    # Ovulation approx 14 days before next period
    ovulation_day = next_period - timedelta(days=14)

    ovulation_start = ovulation_day - timedelta(days=2)
    ovulation_end = ovulation_day + timedelta(days=2)

    # Confidence logic
    if variability <= 2:
        confidence = "high"
        trend = "stable"
    elif variability <= 6:
        confidence = "moderate"
        trend = "slightly_variable"
    else:
        confidence = "low"
        trend = "variable"

    return {
        "next_period_date": next_period,
        "ovulation_window_start": ovulation_start,
        "ovulation_window_end": ovulation_end,
        "prediction_confidence": confidence,
        "trend_direction": trend
    }