def generate_health_alerts(pattern_data, symptom_data, pcos_score, cycles):
    alerts = []

    # 1️⃣ Low Data Warning
    if len(cycles) < 3:
        alerts.append({
            "type": "low_data",
            "severity": "info",
            "message": "More cycle data is needed for reliable health insights."
        })

    # 2️⃣ Long Cycle Alert
    avg = pattern_data.get("average_cycle_length")
    if avg and avg > 45:
        alerts.append({
            "type": "long_cycle",
            "severity": "moderate",
            "message": "Average cycle length is longer than typical range."
        })

    # 3️⃣ High Variability Alert
    variability = pattern_data.get("cycle_variability_days")
    if variability and variability > 10:
        alerts.append({
            "type": "high_variability",
            "severity": "moderate",
            "message": "Cycle length variability is elevated."
        })

    # 4️⃣ Heavy Bleeding Alert
    heavy = symptom_data.get("heavy_bleeding_frequency", 0)
    if heavy > 60:
        alerts.append({
            "type": "heavy_bleeding",
            "severity": "moderate",
            "message": "Frequent heavy bleeding reported."
        })

    # 5️⃣ High PCOS Risk Alert
    if pcos_score >= 0.7:
        alerts.append({
            "type": "high_pcos_risk",
            "severity": "high",
            "message": "PCOS risk score is elevated."
        })

    return alerts