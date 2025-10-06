import serial, serial.tools.list_ports
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

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
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
ax.set_zlim([0, 3])
ax.set_title('Pitch & Roll Visualization')

def create_box():
    x = [-1, 1, 1, -1, -1]
    y = [-1, -1, 1, 1, -1]
    z = [0, 0, 0, 0, 0]
    return np.array([x, y, z])

box = create_box()

def rotation_matrix(roll, pitch):
    r = np.radians(roll)
    p = np.radians(pitch)
    Rx = np.array([[1,0,0],[0,np.cos(r),-np.sin(r)],[0,np.sin(r),np.cos(r)]])
    Ry = np.array([[np.cos(p),0,np.sin(p)],[0,1,0],[-np.sin(p),0,np.cos(p)]])
    return Ry @ Rx

def update(i):
    line = ser.readline().decode().strip()
    if not line: return
    try:
        pitch, roll = map(float, line.split(','))
    except:
        return
    R = rotation_matrix(roll, pitch)
    rotated = R @ box
    ax.cla()
    ax.plot(rotated[0], rotated[1], rotated[2], color='blue')
    ax.set_xlim([-2,2])
    ax.set_ylim([-2,2])
    ax.set_zlim([0,3])
    ax.set_title(f"Pitch={pitch:.1f}°, Roll={roll:.1f}°")
    return

ani = animation.FuncAnimation(fig, update, interval=50)
plt.show()
