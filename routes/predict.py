from fastapi import APIRouter, UploadFile, File, HTTPException
import requests
import os

router = APIRouter(
    prefix="/predict",
    tags=["Prediction"]
)

ML_API_URL = os.getenv(
    "ML_API_URL",
    "http://34.101.66.56:8000/ml/predict"
)

@router.post("/")
async def predict(file: UploadFile = File(...)):
    try:
        response = requests.post(
            ML_API_URL,
            files={
                "file": (
                    file.filename,
                    await file.read(),
                    file.content_type
                )
            },
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=504,
            detail="ML Server Timeout"
        )

    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=503,
            detail=f"Cannot connect to ML Server: {str(e)}"
        )