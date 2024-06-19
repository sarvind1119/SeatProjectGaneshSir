import cv2
import numpy as np 
import torch
import glob
from natsort import natsorted
import subprocess
import os
from ultralytics import YOLO
from PIL import Image
import requests
from io import BytesIO

lst = []
Path = 'seatnumbers/'

image = cv2.imread("c://Users//HP//Downloads//vvk.jpg")

with open("coordinate.txt", "r") as filestream:
		for line in filestream:
			currentline = line.split(" ")
			print(currentline[0])
			seatnum=currentline[0]
			cropped_image = image[int(currentline[1]):int(currentline[2]),int(currentline[3]):int(currentline[4])]
			outfile=Path+seatnum+".jpg"
			cv2.imwrite(outfile,cropped_image)
			#subprocess.call("python detect.py --weights yolov5x.pt --source cropped_image --save-txt", shell=True)
			#os.system("python detect.py --weights yolov5x.pt --source "outfile" --save-txt")
			#os.system('{} {} {} {} {} {} {}'.format("python","detect.py","--weights","yolov5x.pt","--source",outfile,"--save-txt"))
			print(outfile)

			
model = YOLO("yolov8x.pt")			

#model = torch.hub.load("ultralytics/yolov5", "yolov5x")  # or yolov5n - yolov5x6, custom

imgs = [cv2.imread(file) for file in natsorted(glob.glob(Path+"/*.jpg"))]
#imgs="test"

#print('image_array shape:', np.array(imgs).shape[0])

# Inference
results = model.predict(imgs, show=True, save=True, save_txt=True, show_labels=True)

# Results:
print(results[0].boxes.data)

#for result in results:
#    boxes = result.boxes  # Boxes object for bounding box outputs
#    masks = result.masks  # Masks object for segmentation masks outputs
#    keypoints = result.keypoints  # Keypoints object for pose outputs
#    probs = result.probs  # Probs object for classification outputs
#    obb = result.obb  # Oriented boxes object for OBB outputs
#    result.show()  # display to screen
#    result.save(filename="result.jpg")  # save to disk
    
#for r in results:
    #print(r.names)  # print the Boxes object containing the detection bounding boxes
for i, r in enumerate(results):
    # Plot results image
    im_bgr = r.plot()  # BGR-order numpy array
    im_rgb = Image.fromarray(im_bgr[..., ::-1])  # RGB-order PIL image

    # Show results to screen (in supported environments)
    #r.show()

    # Save results to disk
    r.save(filename=f"results{i}.jpg")
        

#yolo task=detect mode=predict model=yolov8x.pt  source=gsm/7.jpg save_txt=True



			
			
