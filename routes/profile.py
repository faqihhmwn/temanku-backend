from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from config import get_db
from repository import profile as profile_repo
from models.profile import ProfileUpdate, ProfileResponse, ChangePasswordRequest
from oauth2 import get_current_user
from fastapi import UploadFile, File
from tables.users import Users
from utils.storage import upload_image, delete_image


router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)


@router.get("/me", response_model=ProfileResponse)
def get_my_profile(
    current_user = Depends(get_current_user)
):
    return current_user


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


@router.put("/photo")
async def upload_profile_photo(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    user = db.query(Users).filter(
        Users.id == current_user.id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="File must be an image"
        )

    # hapus foto lama
    if user.profile_image_url:
        try:
            delete_image(user.profile_image_url)
        except Exception:
            pass

    # upload foto baru
    image_url = upload_image(file)

    user.profile_image_url = image_url

    db.commit()
    db.refresh(user)

    return {
        "success": True,
        "message": "Photo profil berhasil diperbarui",
        "data": {
            "profile_image_url": image_url
        }
    }


@router.delete("/photo")
def delete_profile_photo(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    user = db.query(Users).filter(
        Users.id == current_user.id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user.profile_image_url:
        try:
            delete_image(user.profile_image_url)
        except Exception:
            pass

    db.commit()

    return {
        "success": True,
        "message": "Photo profil berhasil dihapus"
    }


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
        "success": True,
        "message": "Password updated successfully"
    }
