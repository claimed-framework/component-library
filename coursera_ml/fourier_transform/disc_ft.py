"""
(C) 2018 Nikolay Manchev

This work is licensed under the Creative Commons Attribution 4.0 International
License. To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/.
"""


import numpy as np

import matplotlib.pyplot as plt

import math

from numpy.fft import fft


def gen_wave (freq, amp, T, sr):

    time = np.arange(0,T,T/sr)
    
    X = amp*np.sin(2*np.pi*freq*time)
    
    return time,X


plt.style.use("seaborn")
plt.rcParams["xtick.labelsize"] = 14
plt.rcParams["ytick.labelsize"] = 14

f, axarr = plt.subplots(2, figsize=(20, 8))

sr=50 #in Hz

x,y   = gen_wave(3,2,1,sr)
x,y2   = gen_wave(5,3,1,sr)

y = y + y2

axarr[0].plot(x, y)

n = len(y) 
p = fft(y) # take the fourier transform 

mag = np.sqrt(p.real**2 + p.imag**2)

mag = mag * 2 / n

mag = mag[0:math.ceil((n)/2.0)]

x = np.arange(0, len(mag), 1.0) * (sr / n)

axarr[1].bar(x, mag, color='b')
axarr[1].xaxis.set_ticks(np.arange(min(x), max(x)+1, 1.0))

plt.show()





