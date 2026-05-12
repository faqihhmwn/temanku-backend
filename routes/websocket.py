from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import base64
import os
import uuid

from services.predict_service import predict_image


router = APIRouter(
    tags=["WebSocket"]
)


@router.websocket("/ws/predict")
async def websocket_predict(websocket: WebSocket):
    await websocket.accept()

    temp_folder = "temp"
    os.makedirs(temp_folder, exist_ok=True)

    try:
        while True:
            data = await websocket.receive_text()

            # Kalau frontend kirim format data:image/jpeg;base64,...
            if "," in data:
                data = data.split(",")[1]

            image_bytes = base64.b64decode(data)

            file_path = os.path.join(
                temp_folder,
                f"{uuid.uuid4()}.jpg"
            )

            with open(file_path, "wb") as file:
                file.write(image_bytes)

            result = predict_image(file_path)

            if os.path.exists(file_path):
                os.remove(file_path)

            prediction = result.get("prediction")
            confidence = result.get("confidence", 0)

            await websocket.send_json({
                "success": True,
                "type": "translation_result",
                "data": {
                    "prediction": prediction,
                    "confidence": confidence,
                    "is_detected": prediction is not None
                }
            })

    except WebSocketDisconnect:
        print("WebSocket disconnected")