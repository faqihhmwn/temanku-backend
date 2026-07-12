from ultralytics import YOLO
import os


MODEL_PATH = "best.pt"

model = YOLO(MODEL_PATH)


def predict_image(image_path: str):
    results = model(
        image_path,
        conf=0.35,
        iou=0.45,
        verbose=False
    )

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

            x1, y1, x2, y2 = box.xyxy[0].tolist()

            predictions.append({
                "label": class_name,
                "confidence": confidence,
                "bbox": {
                    "x1": float(x1),
                    "y1": float(y1),
                    "x2": float(x2),
                    "y2": float(y2)
                }
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

    # # filter prediction

    # if best_prediction["confidence"] < 0.45:
    #     return {
    #         "prediction": None,
    #         "confidence": best_prediction["confidence"],
    #         "message": "Prediksi tidak stabil"
    #     }

    return {
        "prediction": best_prediction["label"],
        "confidence": round(best_prediction["confidence"], 3),
        "bbox": best_prediction["bbox"],
        "all_predictions": predictions
    }