"""
(C) 2018 Nikolay Manchev

This work is licensed under the Creative Commons Attribution 4.0 International
License. To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/.
"""

import numpy as np

import matplotlib.pyplot as plt

from scipy.io import wavfile

fs, snd = wavfile.read("output.wav")

snd = snd / (2.**15)
s1 = snd[:,0]

plt.figure(figsize=(20, 8))
plt.style.use("seaborn")

time = np.arange(0, s1.shape[0], 1)
time = (time / fs) * 1000

plt.plot(time, s1, color='b')

plt.ylabel('Amplitude', fontsize=16)
plt.xlabel('Time (ms)', fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

plt.show()