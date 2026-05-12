from ultralytics import YOLO
import cv2
import time

# Load model
model = YOLO("../modeling/large/epoch20/weights/best.pt")

cap = cv2.VideoCapture(1)
if not cap.isOpened():
    print("Error: Kamera tidak terdeteksi!")
    exit()

prev_time = 0

# Variabel FPS rata-rata
fps_sum = 0
fps_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    curr_time = time.time()

    # Inferensi
    results = model(frame, verbose=False)
    r = results[0]

    detection_active = False

    # Jika ada deteksi
    if r.boxes is not None and len(r.boxes) > 0:
        detection_active = True
        boxes = r.boxes

        # Ambil confidence tertinggi
        best_idx = boxes.conf.argmax()
        box = boxes.xyxy[best_idx].cpu().numpy()
        conf = boxes.conf[best_idx].item()
        cls = int(boxes.cls[best_idx].item())

        x1, y1, x2, y2 = map(int, box)
        label = f"{model.names[cls]} {conf:.2f}"

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            frame,
            label,
            (x1, y1 - 8),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,   # ukuran font diperkecil
            (0, 255, 0),
            2
        )

    # Hitung FPS sesaat
    fps = 1 / (curr_time - prev_time) if prev_time != 0 else 0
    prev_time = curr_time

    # Catat FPS hanya saat aktif
    if detection_active and fps > 0:
        fps_sum += fps
        fps_count += 1

    # Tampilkan FPS sesaat di layar (kecil)
    cv2.putText(
        frame,
        f"FPS: {fps:.2f}",
        (20, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,   # font kecil
        (0, 255, 0),
        2
    )

    cv2.imshow("YOLOv11 Realtime", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Cetak AVG FPS ke terminal
if fps_count > 0:
    avg_fps = fps_sum / fps_count
    print(f"\nRATA-RATA FPS SAAT AKTIF: {avg_fps:.2f}")
else:
    print("\nTidak ada deteksi, FPS rata-rata tidak dihitung.")
