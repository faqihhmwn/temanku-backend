import os
import cv2
import albumentations as A

# =========================
# KONFIGURASI
# =========================
TRAIN_DIR = r"../dataset_cad/aug/train/img"
IMAGE_EXT = [".jpg", ".jpeg", ".png"]

# =========================
# AUGMENTASI TERPISAH
# =========================
augments = {
    "rotL": A.Rotate(limit=(-15, -15), p=1.0),
    "rotR": A.Rotate(limit=(15, 15), p=1.0),
    "flip": A.HorizontalFlip(p=1.0),
    "brightUp": A.RandomBrightnessContrast(
        brightness_limit=(0.2, 0.2),
        contrast_limit=0,
        p=1.0
    ),
    "brightDown": A.RandomBrightnessContrast(
        brightness_limit=(-0.2, -0.2),
        contrast_limit=0,
        p=1.0
    )
}

# =========================
# PROSES AUGMENTASI
# =========================
for label in os.listdir(TRAIN_DIR):
    label_path = os.path.join(TRAIN_DIR, label)
    if not os.path.isdir(label_path):
        continue

    for filename in os.listdir(label_path):
        name, ext = os.path.splitext(filename)
        if ext.lower() not in IMAGE_EXT:
            continue

        img_path = os.path.join(label_path, filename)
        image = cv2.imread(img_path)
        if image is None:
            continue

        for suffix, aug in augments.items():
            augmented = aug(image=image)
            aug_img = augmented["image"]

            new_name = f"{name}_{suffix}{ext}"
            save_path = os.path.join(label_path, new_name)
            cv2.imwrite(save_path, aug_img)

print("Augmentasi train (5x per gambar) selesai.")
