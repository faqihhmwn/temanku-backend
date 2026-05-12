from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from config import get_db
from tables.dictionary import Dictionary

import shutil
import os

router = APIRouter(
    prefix="/dictionary",
    tags=["Dictionary"]
)


# CREATE
@router.post("/")
async def create_dictionary(
    letter: str,
    description: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_data = Dictionary(
        letter=letter,
        image_url=file_path,
        description=description
    )

    db.add(new_data)
    db.commit()
    db.refresh(new_data)

    return {
        "success": True,
        "message": "Dictionary created",
        "data": new_data
    }


# GET ALL
@router.get("/")
def get_all_dictionary(
    db: Session = Depends(get_db)
):

    data = db.query(Dictionary).all()

    return {
        "success": True,
        "data": data
    }


# GET DETAIL
@router.get("/{dictionary_id}")
def get_dictionary_detail(
    dictionary_id: int,
    db: Session = Depends(get_db)
):

    data = db.query(Dictionary).filter(
        Dictionary.id == dictionary_id
    ).first()

    if not data:
        return {
            "success": False,
            "message": "Dictionary not found"
        }

    return {
        "success": True,
        "data": data
    }


# UPDATE
@router.put("/{dictionary_id}")
async def update_dictionary(
    dictionary_id: int,
    letter: str,
    description: str,
    file: UploadFile = None,
    db: Session = Depends(get_db)
):

    data = db.query(Dictionary).filter(
        Dictionary.id == dictionary_id
    ).first()

    if not data:
        return {
            "success": False,
            "message": "Dictionary not found"
        }

    data.letter = letter
    data.description = description

    if file:

        # delete old image
        if os.path.exists(data.image_url):
            os.remove(data.image_url)

        # save new image
        file_path = f"uploads/{file.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        data.image_url = file_path

    db.commit()
    db.refresh(data)

    return {
        "success": True,
        "message": "Dictionary updated",
        "data": data
    }


# DELETE
@router.delete("/{dictionary_id}")
def delete_dictionary(
    dictionary_id: int,
    db: Session = Depends(get_db)
):

    data = db.query(Dictionary).filter(
        Dictionary.id == dictionary_id
    ).first()

    if not data:
        return {
            "success": False,
            "message": "Dictionary not found"
        }

    # delete image file
    if os.path.exists(data.image_url):
        os.remove(data.image_url)

    db.delete(data)
    db.commit()

    return {
        "success": True,
        "message": "Dictionary deleted"
    }