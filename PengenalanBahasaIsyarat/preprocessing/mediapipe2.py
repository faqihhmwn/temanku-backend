import cv2
import mediapipe as mp
import os

# ======================
# KONFIGURASI
# ======================
IMAGE_DIR = "../dataset_banding/pembagian/val/img/kasih"
LABEL_DIR = "../dataset_banding/pembagian/val/labels/kasih"
CLASS_ID = 27
PADDING = 0.2  # 20% padding bounding box

os.makedirs(LABEL_DIR, exist_ok=True)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=2,          # deteksi 2 tangan
    min_detection_confidence=0.3
)

# ======================
# PROSES SEMUA GAMBAR
# ======================
for img_name in os.listdir(IMAGE_DIR):
    if not img_name.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    img_path = os.path.join(IMAGE_DIR, img_name)
    image = cv2.imread(img_path)
    if image is None:
        continue

    h, w, _ = image.shape
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    # JIKA TIDAK ADA TANGAN → SKIP
    if not results.multi_hand_landmarks:
        print(f"Tangan tidak terdeteksi: {img_name}")
        continue

    # ======================
    # GABUNG SEMUA LANDMARK (1 atau 2 TANGAN)
    # ======================
    all_x = []
    all_y = []

    for hand_landmarks in results.multi_hand_landmarks:
        for lm in hand_landmarks.landmark:
            all_x.append(lm.x)
            all_y.append(lm.y)

    x_min = min(all_x)
    x_max = max(all_x)
    y_min = min(all_y)
    y_max = max(all_y)

    box_width = x_max - x_min
    box_height = y_max - y_min

    # ======================
    # TAMBAH PADDING
    # ======================
    x_min -= box_width * PADDING
    x_max += box_width * PADDING
    y_min -= box_height * PADDING
    y_max += box_height * PADDING

    # jaga di dalam frame (0–1)
    x_min = max(0.0, x_min)
    y_min = max(0.0, y_min)
    x_max = min(1.0, x_max)
    y_max = min(1.0, y_max)

    # ======================
    # FORMAT YOLO (SATU LABEL)
    # ======================
    x_center = (x_min + x_max) / 2
    y_center = (y_min + y_max) / 2
    box_width = x_max - x_min
    box_height = y_max - y_min

    label_name = os.path.splitext(img_name)[0] + ".txt"
    label_path = os.path.join(LABEL_DIR, label_name)

    with open(label_path, "w") as f:
        f.write(
            f"{CLASS_ID} "
            f"{x_center:.6f} "
            f"{y_center:.6f} "
            f"{box_width:.6f} "
            f"{box_height:.6f}"
        )

    # print(f"Label dibuat (1 box gabungan): {label_name}")

hands.close()
print("Selesai membuat label YOLO (dua tangan → satu bounding box).")
