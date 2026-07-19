from fastapi import FastAPI, UploadFile, File
from services.predict_service import predict_image

import os
import shutil
import uuid


app = FastAPI(
    title="Temanku ML Service",
    description="YOLOv11 Sign Language Recognition Service",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "ML Service is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/ml/predict")
async def predict(file: UploadFile = File(...)):

    temp_folder = "temp"
    os.makedirs(temp_folder, exist_ok=True)

    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"

    file_path = os.path.join(
        temp_folder,
        unique_filename
    )

    try:

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

        result = predict_image(file_path)

        return {
            "success": True,
            "message": "Prediction success",
            "data": result
        }

    finally:

        if os.path.exists(file_path):
            os.remove(file_path)