from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from config import get_db
from tables.dictionary import Dictionary
from oauth2 import get_current_admin
from utils.storage import upload_image, delete_image

router = APIRouter(
    prefix="/dictionary",
    tags=["Dictionary"]
)


# CREATE
@router.post("/")
async def create_dictionary(
    name: str,
    category: str,
    description: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):

    # cek duplikat
    existing = db.query(Dictionary).filter(
        Dictionary.name == name
    ).first()

    if existing:
        return {
            "success": False,
            "message": f"Dictionary '{name}' already exists"
        }

    # upload ke Google Cloud Storage
    image_url = upload_image(file)

    new_data = Dictionary(
        name=name,
        category=category,
        image_url=image_url,
        description=description
    )

    db.add(new_data)
    db.commit()
    db.refresh(new_data)

    return {
        "success": True,
        "message": "Dictionary created",
        "data": {
            "id": new_data.id,
            "name": new_data.name,
            "description": new_data.description,
            "category": new_data.category,
            "image_url": new_data.image_url
        }
    }


# GET ALL
@router.get("/")
def get_all_dictionary(
    db: Session = Depends(get_db)
):

    data = db.query(Dictionary).all()

    return {
        "success": True,
        "data": [
            {
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "category": item.category,
                "image_url": item.image_url
            }
            for item in data
        ]
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
        "data": {
            "id": data.id,
            "name": data.name,
            "description": data.description,
            "category": data.category,
            "image_url": data.image_url
        }
    }


# UPDATE
@router.put("/{dictionary_id}")
async def update_dictionary(
    dictionary_id: int,
    name: str,
    category: str,
    description: str,
    file: UploadFile = None,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):

    data = db.query(Dictionary).filter(
        Dictionary.id == dictionary_id
    ).first()

    if not data:
        return {
            "success": False,
            "message": "Dictionary not found"
        }

    # cek duplikat selain dirinya sendiri
    existing = db.query(Dictionary).filter(
        Dictionary.name == name,
        Dictionary.id != dictionary_id
    ).first()

    if existing:
        return {
            "success": False,
            "message": f"Dictionary '{name}' already exists"
        }

    data.name = name
    data.category = category
    data.description = description

    if file:

        # hapus gambar lama dari GCS
        delete_image(data.image_url)

        # upload gambar baru ke GCS
        image_url = upload_image(file)

        data.image_url = image_url

    db.commit()
    db.refresh(data)

    return {
        "success": True,
        "message": "Dictionary updated",
        "data": {
            "id": data.id,
            "name": data.name,
            "description": data.description,
            "category": data.category,
            "image_url": data.image_url
        }
    }


# DELETE
@router.delete("/{dictionary_id}")
def delete_dictionary(
    dictionary_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):

    data = db.query(Dictionary).filter(
        Dictionary.id == dictionary_id
    ).first()

    if not data:
        return {
            "success": False,
            "message": "Dictionary not found"
        }

    # hapus gambar dari GCS
    delete_image(data.image_url)

    db.delete(data)
    db.commit()

    return {
        "success": True,
        "message": "Dictionary deleted"
    }