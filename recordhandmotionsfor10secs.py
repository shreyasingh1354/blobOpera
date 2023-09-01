import cv2
import numpy as np
import csv
from datetime import datetime, timedelta

# Initialize the camera
cap = cv2.VideoCapture(0)

# Create a background subtractor to detect motion
bg_subtractor = cv2.createBackgroundSubtractorMOG2()

# Initialize variables for motion tracking
previous_x, previous_y = 0, 0
motion_direction = ""
motion_speed = 0

# Create a CSV file for recording motion data
csv_file = open('motion_data.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Timestamp", "Direction", "Speed"])

# Calculate the end time (10 seconds from the current time)
end_time = datetime.now() + timedelta(seconds=10)

while datetime.now() < end_time:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Apply background subtraction to detect motion
    fg_mask = bg_subtractor.apply(frame)

    # Apply some morphological operations to clean up the mask
    kernel = np.ones((5, 5), np.uint8)
    fg_mask = cv2.erode(fg_mask, kernel, iterations=1)
    fg_mask = cv2.dilate(fg_mask, kernel, iterations=2)

    # Find contours in the mask
    contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize motion variables
    x, y, w, h = 0, 0, 0, 0
    motion_detected = False

    # Determine motion direction and speed
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        motion_detected = True

        if previous_x != 0 and previous_y != 0:
            delta_x = x - previous_x
            delta_y = y - previous_y

            if abs(delta_x) > abs(delta_y):
                if delta_x > 0:
                    motion_direction = "Right"
                else:
                    motion_direction = "Left"
            else:
                if delta_y > 0:
                    motion_direction = "Downward"
                else:
                    motion_direction = "Upward"

            motion_speed = np.sqrt(delta_x**2 + delta_y**2)

        previous_x, previous_y = x, y

    # Draw rectangles around detected motion areas
    if motion_detected:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the result
    cv2.imshow('Motion Detection', frame)

    # Record motion data to CSV
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    csv_writer.writerow([timestamp, motion_direction, motion_speed])

    # Exit the loop when the specified time has elapsed
    if datetime.now() >= end_time:
        break

    # Check for 'q' key press to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera, close the CSV file, and close the OpenCV window
cap.release()
csv_file.close()
cv2.destroyAllWindows()
