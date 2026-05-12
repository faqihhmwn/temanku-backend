import cv2
import mediapipe as mp
import os

# ======================
# KONFIGURASI
# ======================
IMAGE_DIR = "../dataset_banding/pembagian/val/img/makan"
LABEL_DIR = "../dataset_banding/pembagian/val/labels/makan"
CLASS_ID = 28
PADDING = 0.2  # 20% padding bounding box

os.makedirs(LABEL_DIR, exist_ok=True)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    min_detection_confidence=0.5
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

    # JIKA TIDAK TERDETEKSI TANGAN → SKIP
    if not results.multi_hand_landmarks:
        print(f"Tangan tidak terdeteksi: {img_name}")
        continue

    landmarks = results.multi_hand_landmarks[0].landmark

    # ======================
    # HITUNG BOUNDING BOX DARI LANDMARK
    # ======================
    x_list = [lm.x for lm in landmarks]
    y_list = [lm.y for lm in landmarks]

    x_min = min(x_list)
    x_max = max(x_list)
    y_min = min(y_list)
    y_max = max(y_list)

    # ukuran box awal
    box_width = x_max - x_min
    box_height = y_max - y_min

    # ======================
    # TAMBAH PADDING
    # ======================
    x_min = x_min - box_width * PADDING
    x_max = x_max + box_width * PADDING
    y_min = y_min - box_height * PADDING
    y_max = y_max + box_height * PADDING

    # jaga agar tetap di dalam gambar (0–1)
    x_min = max(0.0, x_min)
    y_min = max(0.0, y_min)
    x_max = min(1.0, x_max)
    y_max = min(1.0, y_max)

    # ======================
    # HITUNG FORMAT YOLO
    # ======================
    x_center = (x_min + x_max) / 2
    y_center = (y_min + y_max) / 2
    box_width = x_max - x_min
    box_height = y_max - y_min

    # ======================
    # SIMPAN LABEL YOLO
    # ======================
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

    # print(f"Label dibuat (padding): {label_name}")

hands.close()
print("Selesai membuat label YOLO dengan padding untuk kelas A.")
