import cv2
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------
# Parameter
# -----------------------------
IMG_PATH = "../dataset_fiks/fiksData/train/images/A_51.jpg"        # path gambar
LABEL_PATH = "../dataset_fiks/fiksData/train/labels/A_51.txt"      # path label YOLO
IMG_SIZE = 640                 # imgsz YOLO

# Load image
img = cv2.imread(IMG_PATH)
if img is None:
    raise FileNotFoundError("Gambar tidak ditemukan")

img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
h, w, _ = img.shape

# Load YOLO label
with open(LABEL_PATH, "r") as f:
    line = f.readline().strip()

cls, xc, yc, bw, bh = map(float, line.split())

# YOLO → pixel coordinates
xc *= w
yc *= h
bw *= w
bh *= h

x1 = int(max(xc - bw / 2, 0))
y1 = int(max(yc - bh / 2, 0))
x2 = int(min(xc + bw / 2, w))
y2 = int(min(yc + bh / 2, h))

# Crop
crop = img[y1:y2, x1:x2]

# Resize langsung ke 640x640
crop_resize = cv2.resize(crop, (IMG_SIZE, IMG_SIZE))

# Show result
plt.figure(figsize=(4, 4))
plt.imshow(crop_resize)
plt.title("Hasil Crop + Resize Langsung (YOLO)")
plt.axis("off")
plt.show()