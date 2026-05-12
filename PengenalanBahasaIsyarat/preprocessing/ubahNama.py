import os

BASE_DIR = "../dataset_cad/fiks/img"   # ganti dengan path dataset kamu

for label in os.listdir(BASE_DIR):
    folder_path = os.path.join(BASE_DIR, label)

    if not os.path.isdir(folder_path):
        continue

    files = sorted(os.listdir(folder_path))
    counter = 1

    for filename in files:
        old_path = os.path.join(folder_path, filename)

        if not os.path.isfile(old_path):
            continue

        name, ext = os.path.splitext(filename)

        # hanya rename file gambar
        if ext.lower() not in [".jpg", ".jpeg", ".png"]:
            continue

        new_name = f"{label}_{counter}{ext}"
        new_path = os.path.join(folder_path, new_name)

        os.rename(old_path, new_path)
        counter += 1

print("Rename selesai.")
