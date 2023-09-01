import cv2
import numpy as np

# Initialize the camera
cap = cv2.VideoCapture(0)

# Create a background subtractor to detect motion
bg_subtractor = cv2.createBackgroundSubtractorMOG2()

# Initialize variables for motion tracking
prev_x, prev_y = None, None
speed = None

while True:
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

    # Draw rectangles around detected motion areas (hands)
    for contour in contours:
        if cv2.contourArea(contour) > 1000:  # Adjust the area threshold as needed
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Calculate motion direction and speed
            if prev_x is not None and prev_y is not None:
                dx = x - prev_x
                dy = y - prev_y

                if abs(dx) > abs(dy):
                    if dx > 0:
                        direction = "Right"
                    else:
                        direction = "Left"
                else:
                    if dy > 0:
                        direction = "Down"
                    else:
                        direction = "Up"

                speed = np.sqrt(dx**2 + dy**2)

            prev_x, prev_y = x, y

    # Display the result including motion direction and speed
    if speed is not None:
        cv2.putText(frame, f"Direction: {direction}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Speed: {speed:.2f} pixels/frame", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Hand Motion Detection', frame)

    # Exit the loop when the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
