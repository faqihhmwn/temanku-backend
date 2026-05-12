import cv2
import os

IMAGE_DIR = "../dataset_cad/awal/img"
LABEL_DIR = "../dataset_cad/awal/labels"
OUTPUT_DIR = "../dataset_cad/awal/preview"

os.makedirs(OUTPUT_DIR, exist_ok=True)

for img_name in os.listdir(IMAGE_DIR):
    if not img_name.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    img_path = os.path.join(IMAGE_DIR, img_name)
    label_path = os.path.join(LABEL_DIR, os.path.splitext(img_name)[0] + ".txt")

    # kalau label tidak ada → skip
    if not os.path.exists(label_path):
        print(f"Label tidak ditemukan: {img_name}")
        continue

    image = cv2.imread(img_path)
    if image is None:
        continue

    h, w, _ = image.shape

    # ======================
    # BACA LABEL YOLO
    # ======================
    with open(label_path, "r") as f:
        lines = f.readlines()

    for line in lines:
        class_id, x_c, y_c, bw, bh = map(float, line.split())

        x_center = x_c * w
        y_center = y_c * h
        box_width = bw * w
        box_height = bh * h

        x1 = int(x_center - box_width / 2)
        y1 = int(y_center - box_height / 2)
        x2 = int(x_center + box_width / 2)
        y2 = int(y_center + box_height / 2)

        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            image,
            f"Class {int(class_id)}",
            (x1, max(y1 - 10, 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

    # ======================
    # SIMPAN HASIL
    # ======================
    out_path = os.path.join(OUTPUT_DIR, img_name)
    cv2.imwrite(out_path, image)

    # print(f"Preview dibuat: {out_path}")

print("Selesai membuat preview satu folder.")
