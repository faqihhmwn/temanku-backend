import os
import random
import shutil

# =========================
# KONFIGURASI
# =========================
SOURCE_DIR = r"../dataset_cad/fiks/img"
DEST_DIR = r"../dataset_cad/aug"

SPLIT = {
    "train": 0.7,
    "val": 0.15,
    "test": 0.15
}

IMAGE_EXT = [".jpg", ".jpeg", ".png"]

random.seed(42)  # agar hasil konsisten

# =========================
# PROSES SPLIT
# =========================
for label in os.listdir(SOURCE_DIR):
    label_path = os.path.join(SOURCE_DIR, label)

    if not os.path.isdir(label_path):
        continue

    images = [
        f for f in os.listdir(label_path)
        if os.path.splitext(f)[1].lower() in IMAGE_EXT
    ]

    random.shuffle(images)

    total = len(images)
    train_end = int(total * SPLIT["train"])
    val_end = train_end + int(total * SPLIT["val"])

    splits = {
        "train": images[:train_end],
        "val": images[train_end:val_end],
        "test": images[val_end:]
    }

    for split_name, split_files in splits.items():
        target_dir = os.path.join(DEST_DIR, split_name, "img", label)
        os.makedirs(target_dir, exist_ok=True)

        for file in split_files:
            src = os.path.join(label_path, file)
            dst = os.path.join(target_dir, file)

            # copy agar data asli aman
            shutil.copy2(src, dst)

print("Pembagian dataset selesai.")
