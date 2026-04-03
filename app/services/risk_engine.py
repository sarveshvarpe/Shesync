def calculate_pcos_risk(pattern_data, symptom_data):
    """
    Deterministic PCOS risk scoring.
    Score range: 0.0 – 1.0
    """

    score = 0.0

    # Irregular cycles
    if pattern_data.get("irregular"):
        score += 0.35

    # Long cycle average
    avg = pattern_data.get("average_cycle_length")
    if avg and avg > 35:
        score += 0.25

    # Acne frequency %
    acne = symptom_data.get("acne_frequency", 0)
    if acne > 60:
        score += 0.2

    # Severe PMS frequency %
    pms = symptom_data.get("pms_frequency", 0)
    if pms > 60:
        score += 0.1

    # Weight fluctuation indicator
    if symptom_data.get("weight_instability"):
        score += 0.1

    return round(min(score, 1.0), 2)


def categorize_risk(score):
    if score >= 0.7:
        return "high"
    elif score >= 0.4:
        return "moderate"
    elif score > 0:
        return "low"
    return "minimal"