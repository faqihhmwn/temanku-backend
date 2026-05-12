import cv2
import os

IMG_BASE = "../dataset_cad/fiksAug/train/img"
LABEL_BASE = "../dataset_cad/fiksAug/train/labels"
PREVIEW_BASE = "../dataset_cad/fiksAug/train/preview"

os.makedirs(PREVIEW_BASE, exist_ok=True)

for cls in os.listdir(IMG_BASE):
    img_dir = os.path.join(IMG_BASE, cls)
    label_dir = os.path.join(LABEL_BASE, cls)
    preview_dir = os.path.join(PREVIEW_BASE, cls)

    if not os.path.isdir(img_dir):
        continue

    os.makedirs(preview_dir, exist_ok=True)

    for img_name in os.listdir(img_dir):
        if not img_name.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        img_path = os.path.join(img_dir, img_name)
        label_path = os.path.join(label_dir, os.path.splitext(img_name)[0] + ".txt")

        # kalau label tidak ada → skip
        if not os.path.exists(label_path):
            print(f"[SKIP] Label tidak ditemukan: {cls}/{img_name}")
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
        # SIMPAN PREVIEW
        # ======================
        out_path = os.path.join(preview_dir, img_name)
        cv2.imwrite(out_path, image)

print("Selesai membuat preview untuk semua kelas.")
