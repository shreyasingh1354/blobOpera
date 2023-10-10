import pandas as pd
import numpy as np 
from pydub import AudioSegment
from pydub.playback import play
import os

filename = 'santa.wav'
sound = AudioSegment.from_file(filename, format=filename[-3:])

csv_file_path = r'C:\Users\Sachin\9hacks\motion_data.csv'
df = pd.read_csv(csv_file_path)

output_folder = 'audio_box'
file_count = 0
for index, row in df.iterrows():
    speed = min(max(row['Speed'], 1),6)  # Limit the speed to a reasonable range (e.g., 1 to 100)
    speed = row['Speed']  
    octaves = (speed * 100) % 6
    new_sample_rate = int(sound.frame_rate * (3.0 ** octaves))
    hipitch_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
    hipitch_sound = hipitch_sound.set_frame_rate(44100)
    #export / save pitch changed sound
    output_file_path = os.path.join(output_folder, f"octave{file_count}.wav")
    hipitch_sound.export(output_file_path, format="wav")
    file_count= file_count + 1
    if (file_count > 50):
        break

    

