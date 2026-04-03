def generate_personalized_recommendations(
    pattern_data,
    symptom_data,
    risk_level,
    phase_data,
    fertility_score,
    confidence
):
    recommendations = []

    phase = phase_data.get("current_phase")

    # --------------------------------
    # 1️⃣ Phase-Based Guidance
    # --------------------------------
    if phase == "menstrual":
        recommendations.append(
            "Prioritize rest, hydration, and iron-rich foods during menstruation."
        )

    elif phase == "follicular":
        recommendations.append(
            "Engage in skill-building, cardio, or learning activities during follicular phase."
        )

    elif phase == "ovulatory":
        recommendations.append(
            "High-intensity workouts and social engagement may align well with ovulatory phase."
        )

    elif phase == "luteal":
        recommendations.append(
            "Reduce caffeine and increase magnesium-rich foods to support luteal stability."
        )

    # --------------------------------
    # 2️⃣ Risk-Based Prevention
    # --------------------------------
    if risk_level == "moderate":
        recommendations.append(
            "Maintain balanced blood sugar levels through consistent meal timing."
        )
    elif risk_level == "high":
        recommendations.append(
            "Consider medical consultation for hormonal evaluation."
        )
        recommendations.append(
            "Strength training may improve metabolic hormone sensitivity."
        )

    # --------------------------------
    # 3️⃣ Variability Stability
    # --------------------------------
    if pattern_data.get("irregular"):
        recommendations.append(
            "Maintain consistent sleep schedule to support circadian hormone regulation."
        )

    # --------------------------------
    # 4️⃣ Fertility Support
    # --------------------------------
    if fertility_score < 60:
        recommendations.append(
            "Cycle regularity improvements may enhance fertility predictability."
        )

    # --------------------------------
    # 5️⃣ Data Confidence Coaching
    # --------------------------------
    if confidence == "low":
        recommendations.append(
            "Log symptoms consistently to improve personalization accuracy."
        )

    return recommendations