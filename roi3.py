import cv2
import csv

def define_rois(image_path, csv_path):
    """
    Allows user to define multiple Regions of Interest (ROIs) on the image.
    User can enter seat number for each ROI and continue until they choose to quit.

    Parameters:
    image_path (str): Path to the image on which ROIs are to be defined.
    csv_path (str): Path to the CSV file where ROIs and statuses will be saved.
    """
    image = cv2.imread(image_path)
    rois = []

    # Open CSV file in append mode
    with open(csv_path, mode='a', newline='') as csvfile:
        fieldnames = ['seat_number', 'seat_coordinates', 'status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # If file is empty, write the header
        if csvfile.tell() == 0:
            writer.writeheader()

        while True:
            # Ask for seat number
            seatnum = input('Enter seat number (or "q" to quit): ')
            if seatnum.lower() == 'q':
                break

            # Select ROI
            r = cv2.selectROI("Select the area", image, fromCenter=False, showCrosshair=True)

            # If a valid ROI is selected, add it to the list and save to CSV
            if r[2] > 0 and r[3] > 0:
                coordinates = [int(r[1]), int(r[1] + r[3]), int(r[0]), int(r[0] + r[2])]
                rois.append((seatnum, coordinates))
                writer.writerow({'seat_number': seatnum, 'seat_coordinates': coordinates, 'status': 'Unknown'})

                # Crop image and save it
                cropped_image = image[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
                outfile = "seats/" + seatnum + ".jpg"
                cv2.imwrite(outfile, cropped_image)
                print(f"Saved cropped image to: {outfile}")

            cv2.destroyWindow("Select the area")

    return rois

def main():
    image_path = "c://Users//HP//Downloads//vvk.jpg"  # Path to the image where ROIs need to be defined
    csv_path = "seat_coordinates.csv"  # Path to the CSV file
    define_rois(image_path, csv_path)
    print("ROIs defined and saved to CSV.")

if __name__ == "__main__":
    main()
