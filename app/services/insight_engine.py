def generate_clinical_insight(
    pattern_data,
    symptom_data,
    pcos_score,
    risk_level,
    phase_data,
    prediction_data,
    confidence
):
    insights = []

    # -----------------------------
    # 1️⃣ Risk-Based Insight
    # -----------------------------
    if risk_level == "low":
        insights.append(
            "Your current PCOS risk indicators are low based on available cycle and symptom data."
        )
    elif risk_level == "moderate":
        insights.append(
            "Some indicators suggest moderate PCOS-related patterns. Monitoring consistency and lifestyle factors may be beneficial."
        )
    else:
        insights.append(
            "Multiple indicators suggest elevated PCOS-related patterns. A medical consultation may help clarify underlying causes."
        )

    # -----------------------------
    # 2️⃣ Phase-Based Insight
    # -----------------------------
    phase = phase_data.get("current_phase")

    if phase == "menstrual":
        insights.append(
            "You are in the menstrual phase. Rest and iron-rich nutrition may support recovery."
        )
    elif phase == "follicular":
        insights.append(
            "You are in the follicular phase. Energy, focus, and motivation may gradually increase."
        )
    elif phase == "ovulatory":
        insights.append(
            "You are in the ovulatory window. This phase is often associated with peak hormonal balance."
        )
    elif phase == "luteal":
        insights.append(
            "You are in the luteal phase. Emotional sensitivity or PMS-like symptoms may increase."
        )

    # -----------------------------
    # 3️⃣ Variability Stability
    # -----------------------------
    if not pattern_data.get("irregular"):
        insights.append(
            "Your cycle variability currently appears stable."
        )
    else:
        insights.append(
            "Your cycle shows irregular patterns. Tracking consistently may improve insight accuracy."
        )

    # -----------------------------
    # 4️⃣ Prediction Confidence Coaching
    # -----------------------------
    prediction_conf = prediction_data.get("prediction_confidence")

    if prediction_conf == "low":
        insights.append(
            "Prediction accuracy is currently limited due to data variability."
        )
    elif prediction_conf == "high":
        insights.append(
            "Your prediction reliability is strong based on stable historical patterns."
        )

    # -----------------------------
    # 5️⃣ Data Confidence Coaching
    # -----------------------------
    if confidence == "low":
        insights.append(
            "Adding more confirmed cycles will significantly improve personalization accuracy."
        )
    elif confidence == "moderate":
        insights.append(
            "Your data quality is improving. Continued tracking will enhance predictive precision."
        )

    return insights