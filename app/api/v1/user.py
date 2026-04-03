from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.models.user import User

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/me")
def get_current_user_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "age": current_user.age
    }


@router.put("/update")
def update_profile(
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "name" in data:
        current_user.name = data["name"]

    if "age" in data:
        current_user.age = data["age"]

    db.commit()
    db.refresh(current_user)

    return {"message": "Profile updated successfully"}