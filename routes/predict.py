from fastapi import APIRouter, UploadFile, File
import requests

router = APIRouter(
    prefix="/predict",
    tags=["Prediction"]
)

ML_API_URL = "http://34.101.86.173:8000/ml/predict"


@router.post("/")
async def predict(file: UploadFile = File(...)):
    
    response = requests.post(
        ML_API_URL,
        files={
            "file": (
                file.filename,
                await file.read(),
                file.content_type
            )
        }
    )

    return response.json()