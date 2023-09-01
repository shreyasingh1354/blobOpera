import pandas as pd
import numpy as np 
from pydub import AudioSegment
from pydub.playback import play
filename = 'music2.wav'
sound = AudioSegment.from_file(filename, format=filename[-3:])

csv_file_path = r'C:\Users\Sachin\9hacks\motion_data.csv'
df = pd.read_csv(csv_file_path)

for index, row in df.iterrows():
    speed = min(max(row['Speed'], 1), 20)  # Limit the speed to a reasonable range (e.g., 1 to 100)
    speed = row['Speed']  
    if(speed%2==0):
        octaves = speed / 100.0
        new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
        hipitch_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
        hipitch_sound = hipitch_sound.set_frame_rate(44100)
        #export / save pitch changed sound
        hipitch_sound.export(f"octave_{octaves}.wav", format="wav")