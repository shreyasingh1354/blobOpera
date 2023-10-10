import cv2
import mido
import numpy as np
from mido import MidiFile, MidiTrack, Message

# Define MIDI output port (replace 'your_midi_output_port_name' with your MIDI output port)
output_port = mido.open_output('Microsoft GS Wavetable Synth 0')

# Define MIDI mapping parameters
min_note = 60  # MIDI note C4
max_note = 80  # MIDI note G5
min_velocity = 30  # Minimum MIDI velocity
max_velocity = 100  # Maximum MIDI velocity

# Create a video capture object (0 represents the default camera)
cap = cv2.VideoCapture(0)

# Set the camera resolution to a default value (adjust as needed)
cap.set(3, 640)  # Width
cap.set(4, 480)  # Height

# Define hand tracking parameters using OpenCV
import mediapipe as mp
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

while True:
    ret, frame = cap.read()  # Capture a frame from the camera

    # Convert the frame to RGB format for Mediapipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Perform hand tracking with Mediapipe
    results = hands.process(rgb_frame)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get the x-coordinate of the hand (for simplicity, use just one hand)
            hand_x = int(hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x * frame.shape[1])
            
            # Map hand position to MIDI note and velocity
            note = int(np.interp(hand_x, [0, frame.shape[1]], [min_note, max_note]))
            velocity = int(np.interp(hand_x, [0, frame.shape[1]], [min_velocity, max_velocity]))
            
            # Send MIDI note-on message
            output_port.send(Message('note_on', note=note, velocity=velocity))

    # Display the frame (for visualization)
    cv2.imshow('Hand Motion to MIDI', frame)
    
    # Break the loop when a key is pressed (e.g., 'q')
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the MIDI output port
cap.release()
cv2.destroyAllWindows()
output_port.close()

