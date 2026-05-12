import os
import shutil

# ======================
# PATH KONFIGURASI
# ======================
SOURCE_DATASET = "../dataset_banding/Pembagian"          # folder dataset lama
TARGET_DATASET = "../dataset_banding/fiks"     # folder dataset baru

SPLITS = ["Train", "Val", "Test"]

# ======================
# BUAT FOLDER OUTPUT
# ======================
for split in ["train", "val", "test"]:
    os.makedirs(os.path.join(TARGET_DATASET, split, "images"), exist_ok=True)
    os.makedirs(os.path.join(TARGET_DATASET, split, "labels"), exist_ok=True)

# ======================
# PROSES KONVERSI
# ======================
for split in SPLITS:
    img_root = os.path.join(SOURCE_DATASET, split, "Img")
    lbl_root = os.path.join(SOURCE_DATASET, split, "Labels")

    out_split = split.lower()
    out_img = os.path.join(TARGET_DATASET, out_split, "images")
    out_lbl = os.path.join(TARGET_DATASET, out_split, "labels")

    for class_name in os.listdir(img_root):
        img_class_dir = os.path.join(img_root, class_name)
        lbl_class_dir = os.path.join(lbl_root, class_name)

        if not os.path.isdir(img_class_dir):
            continue

        for img_file in os.listdir(img_class_dir):
            if not img_file.lower().endswith((".jpg", ".png", ".jpeg")):
                continue

            src_img = os.path.join(img_class_dir, img_file)
            src_lbl = os.path.join(lbl_class_dir, img_file.replace(".jpg", ".txt"))

            # Copy image
            shutil.copy(src_img, os.path.join(out_img, img_file))

            # Copy label (jika ada)
            if os.path.exists(src_lbl):
                shutil.copy(src_lbl, os.path.join(out_lbl, os.path.basename(src_lbl)))
            else:
                print(f"[WARNING] Label tidak ditemukan: {src_lbl}")

print("✅ Dataset berhasil dikonversi ke format YOLO")
