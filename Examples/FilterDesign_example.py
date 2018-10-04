import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import FilterDesign as fd
import numpy as np
import matplotlib.pyplot as plt

"""Create signal with 3 distinct frequencies"""
x = np.zeros(1000)
for i in range(len(x)):
    x[i] = np.cos(np.pi/25*i) + np.cos(2*np.pi/25*i) + np.cos(np.pi/5*i)

"""Create low pass butterworth to filter out high frequencies"""
low_pass = fd.Butterworth_filter(sampling_period = 0.002,
                                 filter_order = 7,
                                 analog_cutoff_freq = 13,
                                 DC_Gain = 1)

"""Apply filter"""
y = low_pass.apply(x)

"""Plot filtered data"""
plt.plot(y[1:300])
plt.plot(x[1:300])
plt.show()
