import librosa
import librosa.display
import matplotlib.pyplot as plt
import soundfile
import numpy as np
import scipy.signal as sp

def showGraph(s, sampling_rate, title):
	plt.figure(title)
	librosa.display.waveplot(y=s, sr=sampling_rate)
	plt.xlabel("Time (seconds) -->")
	plt.ylabel("Amplitude")

filename_flu = "../IRs/mic_A_/IR1_micA.wav"
flu, _ = librosa.core.load(filename_flu, sr = 96000, mono = True, dtype='float32')
filename_frd = "../IRs/mic_A_/IR2_micA.wav"
frd, _ = librosa.core.load(filename_frd, sr = 96000, mono = True, dtype='float32')
filename_bru = "../IRs/mic_A_/IR3_micA.wav"
bru, _ = librosa.core.load(filename_bru, sr = 96000, mono = True, dtype='float32')
filename_bld = "../IRs/mic_A_/IR4_micA.wav"
bld, _ = librosa.core.load(filename_bld, sr = 96000, mono = True, dtype='float32')
print("Loaded files...")

"""
showGraph(flu, 96000, "FLU")
showGraph(frd, 96000, "FRD")
showGraph(bru, 96000, "BRU")
showGraph(bld, 96000, "BLD")

plt.show()
"""

w_ir = flu + frd + bru + bld
x_ir = flu + frd - bru - bld
y_ir = flu - frd - bru + bld
z_ir = flu - frd + bru - bld

with soundfile.SoundFile('results/IR_w.wav', 'w', 96000, 1, 'PCM_24') as f:
	f.write(w_ir.T)
with soundfile.SoundFile('results/IR_x.wav', 'w', 96000, 1, 'PCM_24') as f:
	f.write(x_ir.T)
with soundfile.SoundFile('results/IR_y.wav', 'w', 96000, 1, 'PCM_24') as f:
	f.write(y_ir.T)
with soundfile.SoundFile('results/IR_z.wav', 'w', 96000, 1, 'PCM_24') as f:
	f.write(z_ir.T)

print("IR converted in B format")
"""
showGraph(w_ir, 96000, "W")
showGraph(x_ir, 96000, "X")
showGraph(y_ir, 96000, "Y")
showGraph(z_ir, 96000, "Z")

plt.show()
"""
file_path = "Zucchero - Freedom.flac"
song, _ = librosa.core.load(file_path, sr = 96000, mono = True, dtype='float32')

phi = -0.285117735173
delta = 0

w_song = song                                
x_song = song * np.cos(phi) * np.cos(delta)                
y_song = song * np.sin(phi) * np.cos(delta)
z_song = song * np.sin(delta)
total = np.array([w_song, y_song, z_song, x_song])
with soundfile.SoundFile('results/Zucchero_spatialized.wav', 'w', 96000, 4, 'PCM_24') as f:
	f.write(total.T)

print("Zucchero spatialized")

w_final = sp.convolve(w_song, w_ir, "same")
x_final = sp.convolve(x_song, x_ir, "same")
y_final = sp.convolve(y_song, y_ir, "same")
z_final = sp.convolve(z_song, z_ir, "same")

w_final = w_final/np.max(np.abs(w_final))
x_final = x_final/np.max(np.abs(x_final))
y_final = y_final/np.max(np.abs(y_final))
if delta!=0:
    z_final = z_final/np.max(np.abs(z_final))

total = np.array([w_final, y_final, z_final, x_final])
with soundfile.SoundFile('results/Zucchero_spatialized_reverberated.wav', 'w', 96000, 4, 'PCM_24') as f:
	f.write(total.T)

with soundfile.SoundFile('results/Zucchero_spatialized_reverberated_w.wav', 'w', 96000, 1, 'PCM_24') as f:
	f.write(w_final.T)
with soundfile.SoundFile('results/Zucchero_spatialized_reverberated_x.wav', 'w', 96000, 1, 'PCM_24') as f:
	f.write(x_final.T)
with soundfile.SoundFile('results/Zucchero_spatialized_reverberated_y.wav', 'w', 96000, 1, 'PCM_24') as f:
	f.write(y_final.T)
with soundfile.SoundFile('results/Zucchero_spatialized_reverberated_z.wav', 'w', 96000, 1, 'PCM_24') as f:
	f.write(z_final.T)
"""
soundfile.write("W_song.wav", w, 96000)
soundfile.write("X_song.wav", x, 96000)
soundfile.write("Y_song.wav", y, 96000)
soundfile.write("Z_song.wav", z, 96000)
"""