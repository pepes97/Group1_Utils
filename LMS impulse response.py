#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 17:36:34 2021

@author: leo
"""

import numpy as np
import scipy.signal as sp
import matplotlib.pyplot as plt
from scipy.io import wavfile
import librosa
from scipy import signal
from scipy.io.wavfile import write
from tqdm import tqdm

plt.close('all')

#### Algoritmo LMS ###

def lms(x, d, w, mu, xw):
    BlkSize = len(x)
    e = np.zeros(BlkSize)
    y = np.zeros(BlkSize)
    for n in range(BlkSize) :
        xw[1:] = xw[:-1] #delay line
        xw[0] = x[n]
        y[n] = w@xw
        e[n] = d[n] - y[n]
        w += mu * (e[n]*xw)
    return y, e

### Loading dei segnali utilizzati ###
x, rate_x = librosa.load('x.wav',sr=44100, mono=True) # segnale in ingresso
plt.plot(x)
plt.figure()
x=x[:50000]
d, rate_d = librosa.load('d.wav', sr=44100, mono=True) # segnale desiderato
plt.plot(d)
d=d[:50000]
print(len(x))
voice, rate_v = librosa.load('woman_voice.wav', sr=48000, mono=True)

### Paramtri del modello ###
N = len(x)
nAverage = 100 #numero di volte che eseguo il test, ovvero farò 30 prove e poi ne farò la media dato che è un mean square error


### Parametri del sistema da identificare ###

h_len=4000 #lunghezza del filtro
M =h_len

### 

eQ = np.zeros(N) #inizializzo il rumore quadratico, infatti sto calcolando il mean square error
xw = np.zeros(h_len) #buffer della linea di ritardo
w  = np.zeros(h_len) #pesi del filtro
mu = 0.001 #rate di aggiornamento

for k in tqdm(range(nAverage)):
    print(">", end='')
    w = 0.1*np.random.randn(M) #inizializzo i parametri del filtro
    y, e = lms(x, d, w, mu, xw) #algoritmo least mean square
    eQ += e**2 #per calcolare il mean square error
print("!")  # stampa > ogni volta che viene eseguita una prova, quando vengono eseguite tutte le prove stampa !

MSE = np.zeros(N)
MSE = 10*np.log10(eQ / nAverage) #faccio la media per calcolare il mean square error e lo porto in dB

### Plot dei risultati ###
plt.figure()
plt.plot(MSE, '-r', linewidth = 2)
plt.xlim((0, N))
plt.xlabel('$n$')
plt.ylabel('Average $]$($w$) [dB]')
plt.title('System Identification')
plt.legend(('Average Mse', 'Noise level bound'), loc='best') 
plt.grid(True)

## Convoluzione di un audio di prova con il filtro trovato ###
filtered = signal.convolve(voice, w)
write('output.wav', 48000, filtered)



