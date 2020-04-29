import librosa
import sys

import librosa.display
import matplotlib.pyplot as plt
import numpy as np


class AudioCollector:
    def collect_music(self, music_path, freq=1000):
        song_data, sr = librosa.load(music_path,freq)
        return song_data


"""
audio_data = "H:/Grind and Hustle - Droeloe.egg"
x, sr = librosa.load(audio_data, 1000)

plt.figure(figsize=(14, 5))
librosa.display.waveplot(x, sr=sr)
plt.show()

array_len = len(x)
print("array len :", array_len)

a = 0
music_data = []
for i in range(0, array_len, int(array_len / 1000)):
    music_data.append(np.take(x, i))

print(music_data)

plt.figure(figsize=(14, 5))
plt.plot([i for i in range(len(music_data))], music_data)
plt.show()
"""
