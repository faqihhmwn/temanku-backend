import os

for split in ["train", "val", "test"]:
    img = len(os.listdir(f"../dataset_fiks/fiksData/{split}/images"))
    lbl = len(os.listdir(f"../dataset_fiks/fiksData/{split}/labels"))
    print(split, img, lbl)
