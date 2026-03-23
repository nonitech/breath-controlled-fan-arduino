import serial
import serial.tools.list_ports
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import csv

# ---------- AUTO DETECT ARDUINO ----------
def find_arduino():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "Arduino" in port.description or "CH340" in port.description:
            return port.device
    return None

port = find_arduino()

if port is None:
    print("Arduino not found. Plug it in.")
    exit()
else:
    print(f"Connected to {port}")

ser = serial.Serial(port, 9600)

# ---------- DATA STORAGE ----------
breath_data = []
motor_data = []

# ---------- SMOOTHING FUNCTION ----------
def moving_average(data, window_size=5):
    if len(data) < window_size:
        return data
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

# ---------- SAVE DATA FUNCTION ----------
def save_to_csv():
    with open("data.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Breath", "Motor"])
        for i in range(len(breath_data)):
            writer.writerow([breath_data[i], motor_data[i]])
    print("Data saved to data.csv")

# ---------- PLOT SETUP ----------
fig, ax = plt.subplots()
line1, = ax.plot([], [], label='Raw Breath')
line2, = ax.plot([], [], label='Smoothed Breath', linewidth=2)
line3, = ax.plot([], [], label='Motor Speed', linestyle='dashed')

ax.set_xlim(0, 200)
ax.set_ylim(0, 1100)
ax.set_xlabel("Samples")
ax.set_ylabel("Value")
ax.legend()
ax.grid(True)

# ---------- UPDATE FUNCTION ----------
def update(frame):
    try:
        line = ser.readline().decode().strip()

        if ',' in line:
            breath, motor = line.split(',')
            breath = int(breath)
            motor = int(motor)

            breath_data.append(breath)
            motor_data.append(motor)

            # Keep last 200 samples
            if len(breath_data) > 200:
                breath_data.pop(0)
                motor_data.pop(0)

            x = np.arange(len(breath_data))

            # Smooths signal
            smooth = moving_average(breath_data, 5)
            x_smooth = np.arange(len(smooth))

            line1.set_data(x, breath_data)
            line2.set_data(x_smooth, smooth)
            line3.set_data(x, motor_data)

    except Exception as e:
        print(e)

    return line1, line2, line3

# ---------- CLOSE EVENT ----------
def on_close(event):
    print("Saving data before exit...")
    save_to_csv()

fig.canvas.mpl_connect('close_event', on_close)

ani = animation.FuncAnimation(fig, update, interval=25)
plt.show()
