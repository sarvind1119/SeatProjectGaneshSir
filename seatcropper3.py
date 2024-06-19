import cv2
import numpy as np
import os
import glob
import csv
from natsort import natsorted
from ultralytics import YOLO
from PIL import Image

Path = 'seats/'

# Ensure the output directory exists
if not os.path.exists(Path):
    os.makedirs(Path)

image_path = "c://Users//HP//Downloads//vvk.jpg"
csv_path = "seat_coordinates.csv"

def update_csv_status(csv_path, seatnum, status):
    rows = []
    with open(csv_path, mode='r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['seat_number'] == seatnum:
                row['status'] = status
            rows.append(row)

    with open(csv_path, mode='w', newline='') as csvfile:
        fieldnames = ['seat_number', 'seat_coordinates', 'status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def main():
    # Load ROIs from CSV
    rois = []
    with open(csv_path, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            coordinates = eval(row['seat_coordinates'])
            rois.append((row['seat_number'], coordinates))

    # Process each ROI
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at {image_path}")

    for seatnum, (y1, y2, x1, x2) in rois:
        cropped_image = image[y1:y2, x1:x2]
        outfile = os.path.join(Path, seatnum + ".jpg")
        cv2.imwrite(outfile, cropped_image)
        print(f"Saved cropped image to: {outfile}")

    model = YOLO("yolov8x.pt")

    image_files = natsorted(glob.glob(os.path.join(Path, "*.jpg")))
    print(f"Image files to be loaded: {image_files}")

    imgs = [cv2.imread(file) for file in image_files]
    if not imgs or any(img is None for img in imgs):
        raise ValueError("No valid images found to process.")

    results = model.predict(imgs, show=True, save=True, save_txt=True, show_labels=True)

    for i, r in enumerate(results):
        im_bgr = r.plot()  # BGR-order numpy array
        im_rgb = Image.fromarray(im_bgr[..., ::-1])  # RGB-order PIL image
        r.save(filename=f"results{i}.jpg")

        seatnum = os.path.basename(image_files[i]).split('.')[0]
        status = 'Present' if len(r.boxes.data) > 0 else 'Absent'
        update_csv_status(csv_path, seatnum, status)

if __name__ == "__main__":
    main()
