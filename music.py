import pygame
import time
import os

pygame.init()

audio_directory = "c:\\Users\\Sachin\\9hacks\\audio_box"

# Load all audio files in the specified directory
audio_files = [os.path.join(audio_directory, filename) for filename in os.listdir(audio_directory) if filename.endswith(".wav")]





# audio_files = ["music2.wav", "music3.wav"]

pygame.mixer.init()

current_audio_index = 0
t=0
start_time = time.time()

while current_audio_index < len(audio_files):
    audio_file = audio_files[current_audio_index]
    pygame.mixer.music.load(audio_file)
    start_time += 5 
    t+=5
    # Calculate the start and end times for playback
    end_time = start_time + 5  # 5 seconds of playback
    pygame.mixer.music.play(loops=0, start=t)
    # Adjust start time for the second audio file
    # if current_audio_index == 1:
    #     start_time += 5  # Start 5 seconds later for the second audio
    #     pygame.mixer.music.play(0, start=5.0)  # Play from the 5-second mark
    # else:
    #     pygame.mixer.music.play()

    while time.time() < end_time:
        pygame.time.Clock().tick(60)

    pygame.mixer.music.stop()
    current_audio_index += 1

pygame.quit()