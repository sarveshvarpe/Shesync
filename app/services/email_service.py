import httpx
from app.config import settings


async def send_otp_email(to_email: str, otp: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.brevo.com/v3/smtp/email",
            headers={
                "api-key": settings.BREVO_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "sender": {"email": settings.EMAIL_FROM},
                "to": [{"email": to_email}],
                "subject": "Your SheSync OTP Code",
                "htmlContent": f"""
                <h2>SheSync Verification</h2>
                <p>Your OTP code is:</p>
                <h1>{otp}</h1>
                <p>This code is valid for 5 minutes.</p>
                """
            }
        )

        if response.status_code != 201:
            raise Exception("Failed to send OTP email")