"""
(C) 2018 Nikolay Manchev

This work is licensed under the Creative Commons Attribution 4.0 International
License. To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/.
"""


import numpy as np

import matplotlib.pyplot as plt

import math

from scipy.io import wavfile

from numpy.fft import fft

plt.rcParams["xtick.labelsize"] = 14
plt.rcParams["ytick.labelsize"] = 14
plt.style.use("seaborn")

threshold = 800
fs, snd = wavfile.read("output.wav")
y = snd[:,0]

plt.figure(figsize=(20, 8))

n = len(y) 
p = fft(y) 

mag = np.sqrt(p.real**2 + p.imag**2)

mag = mag * 2 / n

mag = mag[0:math.ceil((n)/2.0)]

freq = np.arange(0, len(mag), 1.0) * (fs / n)

if threshold != 0:
    print(np.unique(np.rint(freq[np.in1d(mag, mag[mag>threshold])])))
    mag[mag<threshold]=threshold

plt.plot(freq/1000, mag, color='b')
plt.xticks(np.arange(min(freq/1000), max(freq/1000)+1, 1.0))

plt.show()
