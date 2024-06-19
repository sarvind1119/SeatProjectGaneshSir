import cv2
import numpy as np

def define_rois(image_path):
    """
    Allows user to define multiple Regions of Interest (ROIs) on the image.
    User can enter seat number for each ROI and continue until they choose to quit.

    Parameters:
    image_path (str): Path to the image on which ROIs are to be defined.

    Returns:
    list: A list of ROIs where each ROI is represented as a tuple (seat_number, x, y, w, h).
    """
    image = cv2.imread(image_path)
    rois = []

    while True:
        # Ask for seat number
        seatnum = input('Enter seat number (or "q" to quit): ')
        if seatnum.lower() == 'q':
            break

        # Select ROI
        r = cv2.selectROI("Select the area", image, fromCenter=False, showCrosshair=True)

        # If a valid ROI is selected, add it to the list
        if r[2] > 0 and r[3] > 0:
            rois.append((seatnum, int(r[1]), int(r[1] + r[3]), int(r[0]), int(r[0] + r[2])))
            with open("coordinate.txt", "a") as f:
                f.write('{} {} {} {} {}\n'.format(seatnum, int(r[1]), int(r[1] + r[3]), int(r[0]), int(r[0] + r[2])))

            # Crop image and save it
            cropped_image = image[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
            outfile = "seats/" + seatnum + ".jpg"
            cv2.imwrite(outfile, cropped_image)
            print(f"Saved cropped image to: {outfile}")

        cv2.destroyWindow("Select the area")

    return rois

def main():
    image_path = "c://Users//HP//Downloads//Final.jpeg"  # Path to the image where ROIs need to be defined
    rois = define_rois(image_path)
    print("ROIs defined and saved.")

if __name__ == "__main__":
    main()
