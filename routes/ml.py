from fastapi import APIRouter, UploadFile, File
import shutil
import os
import uuid

from services.predict_service import predict_image


router = APIRouter(
    prefix="/ml",
    tags=["ML"]
)


@router.post("/predict")
async def predict(file: UploadFile = File(...)):

    temp_folder = "temp"
    os.makedirs(temp_folder, exist_ok=True)

    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(temp_folder, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = predict_image(file_path)

    if os.path.exists(file_path):
        os.remove(file_path)

    return {
        "success": True,
        "message": "Prediction success",
        "data": result
    }