from ultralytics import YOLO
import os


MODEL_PATH = "best.pt"

model = YOLO(MODEL_PATH)


def predict_image(image_path: str):
    results = model(image_path)

    predictions = []

    for result in results:
        boxes = result.boxes

        if boxes is None or len(boxes) == 0:
            return {
                "prediction": None,
                "confidence": 0,
                "message": "No object detected"
            }

        for box in boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            class_name = model.names[class_id]

            predictions.append({
                "label": class_name,
                "confidence": confidence
            })

    if len(predictions) == 0:
        return {
            "prediction": None,
            "confidence": 0,
            "message": "No object detected"
        }

    best_prediction = max(
        predictions,
        key=lambda x: x["confidence"]
    )

    return {
        "prediction": best_prediction["label"],
        "confidence": best_prediction["confidence"],
        "all_predictions": predictions
    }