from fastapi import APIRouter, UploadFile, File
import shutil
import os

router = APIRouter(
    prefix="/ml",
    tags=["ML"]
)

model = None


@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    global model

    if model is None:
        from ultralytics import YOLO
        model = YOLO("best.pt")

    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        results = model(file_path)

        predictions = []

        for r in results:
            boxes = r.boxes
            names = r.names

            for box in boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                label = names[cls_id]

                predictions.append({
                    "label": label,
                    "confidence": round(conf, 3)
                })

        # kalau tidak ada deteksi
        if len(predictions) == 0:
            return {
                "success": False,
                "message": "Tidak ada gesture terdeteksi"
            }

        # ambil confidence tertinggi
        best_prediction = max(
            predictions,
            key=lambda x: x["confidence"]
        )

        return {
            "success": True,
            "prediction": best_prediction
        }

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)