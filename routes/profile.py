from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config import get_db
from repository import profile as profile_repo
from models.profile import ProfileUpdate, ProfileResponse, ChangePasswordRequest
from utils.oauth2 import get_current_user
from tables.users import Users 
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)

@router.put("/change-password")
def change_password(
    data: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    result = profile_repo.change_password(
        db,
        current_user.id,
        data.current_password,
        data.new_password
    )

    if result is None:
        raise HTTPException(status_code=404, detail="User not found")

    if result == "wrong_password":
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    return {
        "message": "Password updated successfully"
    }

@router.put("/me", response_model=ProfileResponse)
def update_my_profile(
    data: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    user = profile_repo.update_profile(db, current_user.id, data)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@router.get("/{user_id}", response_model=ProfileResponse)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    user = profile_repo.get_profile(db, user_id)

    if not user:  
        raise HTTPException(status_code=404, detail="User not found")

    return user

# @router.put("/{user_id}")
# def update_profile(user_id: int, data: ProfileUpdate, db: Session = Depends(get_db)):
#     user = profile_repo.update_profile(db, user_id, data)

#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     return {
#         "message": "Profile updated successfully",
#         "data": user
#     }



