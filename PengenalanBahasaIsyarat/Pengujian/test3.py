import cv2
import time
from ultralytics import YOLO

# Load model
model = YOLO("../modeling/nano/epoch50/weights/best.pt")

# Buka webcam
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("❌ Webcam tidak bisa dibuka")
    exit()

fps_list = []
prev_time = time.time()

print("▶️ Running... tekan 'q' untuk berhenti")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Gagal membaca frame")
        break

    start_infer = time.time()

    # Inference YOLO
    results = model(frame, conf=0.5)

    end_infer = time.time()

    # Hitung FPS per frame
    fps = 1 / (end_infer - start_infer)
    fps_list.append(fps)

    # Tampilkan hasil (opsional, boleh dihapus kalau mau pure benchmarking)
    annotated_frame = results[0].plot()
    cv2.imshow("YOLO Realtime Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Hitung FPS rata-rata
avg_fps = sum(fps_list) / len(fps_list) if fps_list else 0

print("\n📊 HASIL PENGUJIAN REAL-TIME")
print(f"Total frame diuji : {len(fps_list)}")
print(f"Rata-rata FPS     : {avg_fps:.2f}")
