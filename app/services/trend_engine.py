def analyze_trends(cycles, logs, pattern_data, pcos_score):
    if len(cycles) < 4:
        return {
            "cycle_length_shift": "insufficient_data",
            "variability_trend": "insufficient_data",
            "symptom_intensity_trend": "insufficient_data",
            "risk_direction": "stable"
        }

    recent_cycles = cycles[-3:]
    older_cycles = cycles[:-3]

    recent_lengths = [c.length for c in recent_cycles if hasattr(c, "length")]
    older_lengths = [c.length for c in older_cycles if hasattr(c, "length")]

    if recent_lengths and older_lengths:
        recent_avg = sum(recent_lengths) / len(recent_lengths)
        older_avg = sum(older_lengths) / len(older_lengths)

        if abs(recent_avg - older_avg) <= 2:
            length_shift = "stable"
        elif recent_avg > older_avg:
            length_shift = "increasing"
        else:
            length_shift = "decreasing"
    else:
        length_shift = "unknown"

    variability = pattern_data.get("cycle_variability_days") or 0

    if variability <= 3:
        variability_trend = "stable"
    elif variability <= 7:
        variability_trend = "mild_increase"
    else:
        variability_trend = "increasing"

    symptom_trend = "stable"
    if logs:
        recent_logs = logs[-10:]
        acne_count = sum(1 for log in recent_logs if getattr(log, "acne", False))
        if acne_count > 5:
            symptom_trend = "rising"

    if pcos_score > 0.6:
        risk_direction = "increasing"
    else:
        risk_direction = "stable"

    return {
        "cycle_length_shift": length_shift,
        "variability_trend": variability_trend,
        "symptom_intensity_trend": symptom_trend,
        "risk_direction": risk_direction
    }