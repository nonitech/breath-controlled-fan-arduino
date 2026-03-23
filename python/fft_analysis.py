import numpy as np
import matplotlib.pyplot as plt
import csv

breath = []

# Load saved data
with open("data.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)  # skip header

    for row in reader:
        breath.append(int(row[0]))

signal = np.array(breath)

# FFT
fft_vals = np.fft.fft(signal)
fft_freq = np.fft.fftfreq(len(signal))

# Plot
plt.figure()
plt.plot(fft_freq, np.abs(fft_vals))
plt.title("Frequency Spectrum (FFT)")
plt.xlabel("Frequency")
plt.ylabel("Amplitude")
plt.grid()
plt.show()
