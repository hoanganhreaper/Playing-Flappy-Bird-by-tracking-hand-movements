import cv2
import numpy as np

def calibrate_pixel_to_cm(image_path, object_width_cm):
    try:
        # Read the calibration image (image with the known object)
        calibration_image = cv2.imread(image_path)

        if calibration_image is None:
            raise Exception("Error loading the calibration image. Please check the file path.")

        # Convert the calibration image to grayscale
        gray_calibration = cv2.cvtColor(calibration_image, cv2.COLOR_BGR2GRAY)

        # Apply GaussianBlur to reduce noise
        blurred_calibration = cv2.GaussianBlur(gray_calibration, (5, 5), 0)

        # Apply thresholding to segment the calibration image
        _, thresh_calibration = cv2.threshold(blurred_calibration, 127, 255, cv2.THRESH_BINARY)

        # Find contours in the calibration image
        contours_calibration, _ = cv2.findContours(thresh_calibration, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Assuming the largest contour corresponds to the known object (black tape)
        max_contour_calibration = max(contours_calibration, key=cv2.contourArea)

        # Find the bounding box around the known object
        x_calibration, y_calibration, w_calibration, h_calibration = cv2.boundingRect(max_contour_calibration)

        # Calculate the pixel-to-centimeter ratio
        pixel_to_cm_ratio = object_width_cm / max(w_calibration, h_calibration)

        return pixel_to_cm_ratio

    except Exception as e:
        print(f"An error occurred during calibration: {e}")
        return None

def get_finger_length_from_video(pixel_to_cm_ratio):
    try:
        # Open a video capture object (0 is typically the default camera)
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            raise Exception("Error opening video capture device. Make sure your camera is connected.")

        while True:
            # Read a frame from the video capture
            ret, frame = cap.read()

            if not ret:
                raise Exception("Error reading frame. Check your camera connection.")

            # Convert the frame to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Apply GaussianBlur to reduce noise and improve accuracy of contour detection
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)

            # Apply thresholding to segment the image
            _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)

            # Find contours in the thresholded image
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Assuming the largest contour corresponds to the finger
            max_contour = max(contours, key=cv2.contourArea)

            # Find the bounding box around the finger
            x, y, w, h = cv2.boundingRect(max_contour)

            # Draw the bounding box on the frame
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Calculate the length of the finger in centimeters (assuming it's the length of the bounding box)
            finger_length_cm = max(w, h) * pixel_to_cm_ratio

            # Display the result
            cv2.imshow('Finger Measurement', frame)

            # Break the loop if 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the video capture object and close the OpenCV windows
        cap.release()
        cv2.destroyAllWindows()

        # Print the final finger length in centimeters
        print(f'The length of the finger is approximately {finger_length_cm:.2f} centimeters.')

    except Exception as e:
        print(f"An error occurred: {e}")

# Path to the calibration image with the known object (black tape)
calibration_image_path = 'img\WIN_20240104_22_52_21_Pro.jpg'

# Width of the known object in centimeters (15mm x 15mm)
object_width_cm = 15

# Calibrate the pixel-to-centimeter ratio
pixel_to_cm_ratio = calibrate_pixel_to_cm(calibration_image_path, object_width_cm)

# Call the function to measure finger length in real-time using the calibrated ratio
if pixel_to_cm_ratio is not None:
    get_finger_length_from_video(pixel_to_cm_ratio)
