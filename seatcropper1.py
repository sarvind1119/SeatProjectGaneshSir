import cv2
import os
import glob
from natsort import natsorted
from ultralytics import YOLO
from PIL import Image

Path = 'seatnumbers/'

# Ensure the output directory exists
if not os.path.exists(Path):
    os.makedirs(Path)

image_path = "c://Users//HP//Downloads//Final.jpeg"
image = cv2.imread(image_path)

# Ensure the image is loaded correctly
if image is None:
    raise FileNotFoundError(f"Image not found at {image_path}")

with open("coordinate.txt", "r") as filestream:
    for line in filestream:
        currentline = line.split(" ")
        print(f"Processing line: {line.strip()}")
        seatnum = currentline[0]
        try:
            y1, y2, x1, x2 = map(int, currentline[1:5])
            print(f"Coordinates: y1={y1}, y2={y2}, x1={x1}, x2={x2}")
            cropped_image = image[y1:y2, x1:x2]
            outfile = os.path.join(Path, seatnum + ".jpg")
            if cv2.imwrite(outfile, cropped_image):
                print(f"Successfully saved cropped image to: {outfile}")
            else:
                print(f"Failed to save cropped image to: {outfile}")
        except ValueError as e:
            print(f"Skipping invalid coordinates in line: {line.strip()}. Error: {e}")
        except Exception as e:
            print(f"Unexpected error processing line {line.strip()}: {e}")

model = YOLO("yolov8x.pt")

image_files = natsorted(glob.glob(os.path.join(Path, "*.jpg")))
print(f"Image files to be loaded: {image_files}")

imgs = [cv2.imread(file) for file in image_files]

if not imgs or any(img is None for img in imgs):
    raise ValueError("No valid images found to process.")

results = model.predict(imgs, show=True, save=True, save_txt=True, show_labels=True)
print(results[0].boxes.data)

for i, r in enumerate(results):
    im_bgr = r.plot()  # BGR-order numpy array
    im_rgb = Image.fromarray(im_bgr[..., ::-1])  # RGB-order PIL image
    r.save(filename=f"results{i}.jpg")
