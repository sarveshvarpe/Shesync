from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Optional

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.user_session import UserSession

from app.schemas.auth_schema import (
    SignupRequest,
    LoginRequest,
    RefreshRequest,
    OTPVerifyRequest,
    TokenResponse,
    MessageResponse
)

from app.security.hash import hash_password, verify_password
from app.security.jwt_handler import (
    create_access_token,
    create_refresh_token,
    decode_token
)

from app.services.otp_service import generate_otp, verify_otp
from app.services.email_service import send_otp_email


router = APIRouter(prefix="/auth", tags=["Authentication"])


# =========================
# SIGNUP
# =========================
@router.post("/signup", response_model=MessageResponse)
async def signup(payload: SignupRequest, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # 🔒 Age Validation (Safe Range)
    if payload.age is not None:
        if payload.age < 10 or payload.age > 50:
            raise HTTPException(
                status_code=400,
                detail="Age must be between 10 and 50"
            )

    user = User(
        name=payload.name,
        email=payload.email,
        password=hash_password(payload.password),
        age=payload.age  # ✅ AGE STORED
    )

    db.add(user)
    db.commit()

    otp = generate_otp(payload.email)
    await send_otp_email(payload.email, otp)

    return {"message": "OTP sent to your email"}


# =========================
# VERIFY OTP
# =========================
@router.post("/verify-otp", response_model=MessageResponse)
def verify_otp_route(payload: OTPVerifyRequest, db: Session = Depends(get_db)):

    if not verify_otp(payload.email, payload.otp):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )

    user = db.query(User).filter(User.email == payload.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_verified = True
    db.commit()

    return {"message": "Account verified successfully"}


# =========================
# LOGIN
# =========================
@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, request: Request, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == payload.email).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(payload.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your account first"
        )

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    session = UserSession(
        user_id=user.id,
        refresh_token=refresh_token,
        device_type="web",
        ip_address=request.client.host
    )

    db.add(session)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


# =========================
# REFRESH TOKEN
# =========================
@router.post("/refresh", response_model=TokenResponse)
def refresh_token(payload: RefreshRequest):

    decoded = decode_token(payload.refresh_token)

    if not decoded or decoded.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    new_access = create_access_token({"sub": decoded.get("sub")})

    return {
        "access_token": new_access,
        "refresh_token": payload.refresh_token,
        "token_type": "bearer"
    }


# =========================
# LOGOUT CURRENT DEVICE
# =========================
@router.post("/logout", response_model=MessageResponse)
def logout(payload: RefreshRequest, db: Session = Depends(get_db)):

    session = db.query(UserSession).filter(
        UserSession.refresh_token == payload.refresh_token
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    db.delete(session)
    db.commit()

    return {"message": "Logged out successfully"}


# =========================
# LOGOUT ALL DEVICES
# =========================
@router.post("/logout-all", response_model=MessageResponse)
def logout_all(current_user: User = Depends(get_current_user),
               db: Session = Depends(get_db)):

    db.query(UserSession).filter(
        UserSession.user_id == current_user.id
    ).delete()

    db.commit()

    return {"message": "Logged out from all devices"}