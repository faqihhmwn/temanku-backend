import os

BASE_DIR = r"..\\dataset_fiks\\fiks\\img\\rumah"

files = sorted(os.listdir(BASE_DIR))
counter = 1

for filename in files:
    old_path = os.path.join(BASE_DIR, filename)

    if not os.path.isfile(old_path):
        continue

    name, ext = os.path.splitext(filename)

    # hanya file gambar
    if ext.lower() not in [".jpg", ".jpeg", ".png"]:
        continue

    new_name = f"rumah_{counter}{ext}"
    new_path = os.path.join(BASE_DIR, new_name)

    if os.path.exists(new_path):
        print(f"Skip {new_name}, sudah ada")
        counter += 1
        continue

    os.rename(old_path, new_path)
    counter += 1

print("Rename selesai.")
