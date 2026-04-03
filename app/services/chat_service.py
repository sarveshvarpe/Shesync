import requests
from sqlalchemy.orm import Session
from typing import Optional

from app.config import settings
from app.models.chat import ChatSession, ChatMessage, MessageRole
from app.models.cycle import Cycle
from app.models.cycle_log import CycleLog

from app.services.pattern_analyzer import analyze_cycle_patterns
from app.services.risk_engine import calculate_pcos_risk, categorize_risk
from app.services.alert_engine import generate_health_alerts
from app.services.health_score_engine import calculate_health_score
from app.services.prediction_engine import generate_cycle_prediction


# ==================================
# CONFIG
# ==================================

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama-3.1-8b-instant"


# ==================================
# SYSTEM PROMPT
# ==================================

SYSTEM_PROMPT = """
You are SheSync AI, a supportive menstrual health assistant.

Your role is to help users understand their menstrual cycle,
symptoms, fertility patterns, and reproductive health insights.

STRICT SAFETY RULES:

1. You are NOT a doctor.
2. Do NOT diagnose medical conditions.
3. Do NOT prescribe medication.
4. Do NOT replace professional medical advice.
5. Avoid definitive medical statements.

Instead use phrases like:
- "This pattern can sometimes be associated with..."
- "It may be worth discussing with a healthcare professional."

Tone Guidelines:
- Calm
- Supportive
- Educational
- Non-judgmental
- Empowering
Give neccessary answers only based on the data provided. If the user asks for information outside of the data, politely explain that you can only provide insights based on the cycle and symptom data available. give detail info if asked
Never create panic. Encourage professional consultation when appropriate.
"""


# ==================================
# RESPONSE CLASSIFIER
# ==================================

def classify_response(text: str):

    medical_keywords = [
        "pcos",
        "endometriosis",
        "thyroid",
        "diagnosis",
        "disorder",
        "treatment",
        "hormone imbalance"
    ]

    text_lower = text.lower()

    if any(word in text_lower for word in medical_keywords):
        return "medical_pattern"

    return "general_health"


# ==================================
# CONFIDENCE ESTIMATOR
# ==================================

def estimate_confidence(cycles):

    if len(cycles) >= 6:
        return "high"

    elif len(cycles) >= 3:
        return "moderate"

    return "low"


# ==================================
# MAIN CHAT ENGINE
# ==================================

def generate_ai_response(
    db: Session,
    user,
    message: str,
    session_id: Optional[int] = None
):

    # ---------------------------------
    # 1️⃣ Get or Create Chat Session
    # ---------------------------------

    if session_id:
        session = db.query(ChatSession).filter(
            ChatSession.id == session_id,
            ChatSession.user_id == user.id
        ).first()
    else:
        session = None

    if not session:

        session = ChatSession(
            user_id=user.id,
            title="Health Chat"
        )

        db.add(session)
        db.commit()
        db.refresh(session)


    # ---------------------------------
    # 2️⃣ Save User Message
    # ---------------------------------

    user_msg = ChatMessage(
        session_id=session.id,
        role=MessageRole.user,
        content=message
    )

    db.add(user_msg)
    db.commit()


    # ---------------------------------
    # 3️⃣ Fetch Cycle Data
    # ---------------------------------

    cycles = db.query(Cycle).filter(
        Cycle.user_id == user.id,
        Cycle.is_confirmed == True
    ).order_by(Cycle.start_date).all()


    # ---------------------------------
    # 4️⃣ Analyze Cycle Patterns
    # ---------------------------------

    pattern_data = analyze_cycle_patterns(cycles)


    # ---------------------------------
    # 5️⃣ Cycle Prediction
    # ---------------------------------

    prediction_data = generate_cycle_prediction(
        cycles,
        pattern_data
    )


    # ---------------------------------
    # 6️⃣ Fetch Symptom Logs
    # ---------------------------------

    logs = db.query(CycleLog).filter(
        CycleLog.user_id == user.id
    ).all()

    total_logs = len(logs)

    acne_count = 0
    pms_count = 0
    weight_flag = False
    heavy_bleeding_count = 0

    for log in logs:

        if getattr(log, "acne", False):
            acne_count += 1

        if getattr(log, "severe_pms", False):
            pms_count += 1

        if getattr(log, "weight_instability", False):
            weight_flag = True

        if getattr(log, "heavy_bleeding", False):
            heavy_bleeding_count += 1


    symptom_data = {

        "acne_frequency": (acne_count / total_logs * 100) if total_logs else 0,

        "pms_frequency": (pms_count / total_logs * 100) if total_logs else 0,

        "weight_instability": weight_flag,

        "heavy_bleeding_frequency":
        (heavy_bleeding_count / total_logs * 100) if total_logs else 0
    }


    # ---------------------------------
    # 7️⃣ Risk Engine
    # ---------------------------------

    pcos_score = calculate_pcos_risk(pattern_data, symptom_data)

    risk_level = categorize_risk(pcos_score)

    confidence_level = estimate_confidence(cycles)


    alerts = generate_health_alerts(
        pattern_data,
        symptom_data,
        pcos_score,
        cycles
    )


    health_score = calculate_health_score(
        pattern_data,
        symptom_data,
        pcos_score
    )


    # ---------------------------------
    # 8️⃣ Clinical Context
    # ---------------------------------

    context_block = f"""
User Health Clinical Summary (Backend Calculated)

Cycle Data:
- Total Confirmed Cycles: {len(cycles)}
- Average Cycle Length: {pattern_data.get("average_cycle_length", "N/A")}
- Cycle Variability (days): {pattern_data.get("cycle_variability_days", "N/A")}
- Irregular Pattern: {pattern_data.get("irregular", "N/A")}

Prediction:
- Next Predicted Period: {prediction_data.get("next_period_date", "Unknown")}
- Ovulation Window Start: {prediction_data.get("ovulation_window_start", "Unknown")}
- Ovulation Window End: {prediction_data.get("ovulation_window_end", "Unknown")}

Symptom Analysis:
- Acne Frequency: {round(symptom_data["acne_frequency"], 1)}%
- Severe PMS Frequency: {round(symptom_data["pms_frequency"], 1)}%
- Heavy Bleeding Frequency: {round(symptom_data["heavy_bleeding_frequency"], 1)}%
- Weight Instability: {symptom_data["weight_instability"]}

PCOS Risk Assessment:
- Risk Score: {pcos_score}
- Risk Category: {risk_level}
- Confidence Level: {confidence_level}

Guidance:
Explain insights clearly using the data above.
Avoid diagnosing medical conditions.
Encourage professional consultation if risk is moderate or high.
"""


    # ---------------------------------
    # 9️⃣ Conversation History
    # ---------------------------------

    history_messages = db.query(ChatMessage).filter(
        ChatMessage.session_id == session.id
    ).order_by(ChatMessage.created_at).all()

    formatted_history = [

        {"role": msg.role.value, "content": msg.content}

        for msg in history_messages
    ]


    # ---------------------------------
    # 🔟 Construct Prompt
    # ---------------------------------

    messages = [

        {"role": "system", "content": SYSTEM_PROMPT},

        {"role": "system", "content": context_block}
    ]

    messages.extend(formatted_history)


    # ---------------------------------
    # 11️⃣ Call Groq API
    # ---------------------------------

    headers = {

        "Authorization": f"Bearer {settings.GROQ_API_KEY}",

        "Content-Type": "application/json"
    }

    payload = {

        "model": MODEL_NAME,

        "messages": messages,

        "temperature": 0.7
    }

    response = requests.post(
        GROQ_API_URL,
        headers=headers,
        json=payload
    )


    # ---------------------------------
    # 12️⃣ Handle API Failure Safely
    # ---------------------------------

    if response.status_code != 200:

        ai_reply = (
            "I'm having trouble accessing the AI service right now. "
            "However, your cycle data is still being tracked. "
            "Please try again shortly."
        )

    else:

        ai_reply = response.json()["choices"][0]["message"]["content"]


    # ---------------------------------
    # 13️⃣ Save Assistant Message
    # ---------------------------------

    assistant_msg = ChatMessage(

        session_id=session.id,

        role=MessageRole.assistant,

        content=ai_reply
    )

    db.add(assistant_msg)

    db.commit()


    # ---------------------------------
    # 14️⃣ Classification
    # ---------------------------------

    response_type = classify_response(ai_reply)


    # ---------------------------------
    # 15️⃣ Structured Output
    # ---------------------------------

    return {

        "session_id": session.id,

        "reply": ai_reply,

        "confidence": confidence_level,

        "health_score": health_score,

        "medical_flag": response_type == "medical_pattern",

        "risk_summary": {

            "pcos_risk_score": pcos_score,

            "risk_level": risk_level
        },

        "alerts": alerts
    }