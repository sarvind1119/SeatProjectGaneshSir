import cv2
import numpy as np
  
# Read image 
image = cv2.imread("c://Users//HP//Downloads//vvk.jpg") 

# Ensure the image is loaded correctly
if image is None:
    raise FileNotFoundError("Image not found at specified path.")

# Ask for seat name
sno = input('Seat Number: ')

# Select ROI 
r = cv2.selectROI("Select the area", image)

# Open the coordinate file in append mode
with open("coordinate.txt", "a") as f:
    f.write('{} {} {} {} {}\n'.format(sno, int(r[1]), int(r[1]+r[3]), int(r[0]), int(r[0]+r[2])))

# Crop the image based on the ROI
cropped_image = image[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]

# Display cropped image
cv2.imshow("Cropped image", cropped_image)

# Save the cropped image
outfile = "seats/" + sno + ".jpg"
cv2.imwrite(outfile, cropped_image)

cv2.waitKey(0)
cv2.destroyAllWindows()
