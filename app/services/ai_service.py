import httpx
from app.config import GEMINI_API_KEY

async def ask_ai(question: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
            params={"key": GEMINI_API_KEY},
            json={
                "contents": [{
                    "parts": [{"text": question}]
                }]
            }
        )
        return response.json()