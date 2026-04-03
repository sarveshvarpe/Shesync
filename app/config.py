import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")
    JWT_SECRET = os.getenv("JWT_SECRET")
    REDIS_URL = os.getenv("REDIS_URL")
    BREVO_API_KEY = os.getenv("BREVO_API_KEY")
    EMAIL_FROM = os.getenv("EMAIL_FROM")
    ENV = os.getenv("ENV", "development")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

settings = Settings()