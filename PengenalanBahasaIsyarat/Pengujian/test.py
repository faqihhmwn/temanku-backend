import cv2
from ultralytics import YOLO

# Load model (ganti dengan model hasil training kamu)
model = YOLO("../modeling/nano/epoch50/weights/best.pt")

# Buka webcam (0 = webcam default)
cap = cv2.VideoCapture(1)

# Cek apakah kamera terbuka
if not cap.isOpened():
    print("❌ Webcam tidak bisa dibuka")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Gagal membaca frame")
        break

    # Inference YOLO
    results = model(frame, conf=0.5)

    # Ambil frame hasil deteksi
    annotated_frame = results[0].plot()

    # Tampilkan ke layar
    cv2.imshow("YOLO Realtime Detection", annotated_frame)

    # Tekan 'q' untuk keluar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resource
cap.release()
cv2.destroyAllWindows()
