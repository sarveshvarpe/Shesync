from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    age: Optional[int] = Field(None, ge=10, le=50)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class OTPVerifyRequest(BaseModel):
    email: EmailStr
    otp: str


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class MessageResponse(BaseModel):
    message: str