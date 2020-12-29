#**                                       
#  Mono to (B-Format) Ambisonics to Stereo 
#**                                       

import librosa
import librosa.display
import matplotlib.pyplot as plt
import soundfile
import numpy as np

def showGraph(s, sampling_rate, title):
	plt.figure(title)
	librosa.display.waveplot(y=s, sr=sampling_rate)
	plt.xlabel("Time (seconds) -->")
	plt.ylabel("Amplitude")

phi = 0
delta = 0

file_path = "song.wav"
s, sampling_rate = librosa.core.load(file_path, sr = 96000, mono = True)

showGraph(s, sampling_rate, "Original")

w = s / np.sqrt(3)                                   
x = s * np.cos(phi) * np.cos(delta)                
y = s * np.sin(phi) * np.cos(delta)
z = s * np.sin(delta)

showGraph(w, sampling_rate, "W")
showGraph(x, sampling_rate, "X")
showGraph(y, sampling_rate, "Y")
showGraph(z, sampling_rate, "Z")
plt.show()

soundfile.write("W_song.wav", w, 96000)
soundfile.write("X_song.wav", x, 96000)
soundfile.write("Y_song.wav", y, 96000)
soundfile.write("Z_song.wav", z, 96000)


'''
file_path = "W_song.wav"
w, _ = librosa.core.load(file_path, sr = 96000, mono = True)
file_path = "X_song.wav"
x, _ = librosa.core.load(file_path, sr = 96000, mono = True)
file_path = "Y_song.wav"
y, _ = librosa.core.load(file_path, sr = 96000, mono = True)
file_path = "Z_song.wav"
z, _ = librosa.core.load(file_path, sr = 96000, mono = True)
'''

# Convert to stereo (audio should be reproduced via headphones)

d = np.array([[1, 1],[1, -1], [0, 0], [0,0]])
dn = np.linalg.pinv(d)

a = np.array([w * np.sqrt(3), x, y, z])
s = np.transpose(np.dot(dn,a))

with soundfile.SoundFile('stereo_song.wav', 'w', 96000, 2, 'PCM_24') as f:
	f.write(s)
