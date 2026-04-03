import random
import redis
from app.config import settings

# Connect to Redis
r = redis.Redis.from_url(settings.REDIS_URL)


def generate_otp(email: str):
    otp = str(random.randint(100000, 999999))
    r.setex(f"otp:{email}", 300, otp)  # 5 minutes expiry
    return otp


def verify_otp(email: str, otp: str):
    stored = r.get(f"otp:{email}")
    if stored and stored.decode() == otp:
        r.delete(f"otp:{email}")
        return True
    return False