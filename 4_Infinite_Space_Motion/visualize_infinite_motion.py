import serial, serial.tools.list_ports
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import numpy as np
from random import random

BAUD = 115200
ports = list(serial.tools.list_ports.comports())
arduino_port = None
for p in ports:
    if "Arduino" in p.description or "CH340" in p.description:
        arduino_port = p.device
        break
if not arduino_port:
    raise SystemExit("Arduino not found!")
ser = serial.Serial(arduino_port, BAUD, timeout=1)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim([-10,10]); ax.set_ylim([-10,10]); ax.set_zlim([-10,10])
ax.set_title('3D Infinite Space Motion')

points = np.random.rand(100,3)*20 - 10

def update(i):
    global points
    line = ser.readline().decode().strip()
    if not line: return
    try:
        pitch, roll, yaw = map(float, line.split(','))
    except:
        return
    shift = np.array([np.sin(np.radians(yaw)), np.sin(np.radians(pitch)), np.sin(np.radians(roll))])
    points += shift * 0.1
    points = np.where(points > 10, -10, points)
    ax.cla()
    ax.scatter(points[:,0], points[:,1], points[:,2], c='cyan', s=10)
    ax.set_xlim([-10,10]); ax.set_ylim([-10,10]); ax.set_zlim([-10,10])
    ax.set_title(f"Exploring Infinite Space (Yaw={yaw:.1f})")
    return

ani = animation.FuncAnimation(fig, update, interval=50)
plt.show()
