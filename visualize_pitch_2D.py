import serial, serial.tools.list_ports
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
from collections import deque

BAUD = 115200
WINDOW = 200

ports = list(serial.tools.list_ports.comports())
arduino_port = None
for p in ports:
    if "Arduino" in p.description or "CH340" in p.description:
        arduino_port = p.device
        break
if not arduino_port:
    raise SystemExit("Arduino not found!")
ser = serial.Serial(arduino_port, BAUD, timeout=1)

pitch_buf = deque(maxlen=WINDOW)
x_idx = deque(maxlen=WINDOW)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9,5))
line_pitch, = ax1.plot([], [], label="Pitch (°)")
ax1.set_xlim(0, WINDOW)
ax1.set_ylim(-90, 90)
ax1.legend()
ax1.set_title("MPU6050 Pitch")

bar = Rectangle((-1.5, -0.1), 3.0, 0.2)
ax2.add_patch(bar)
ax2.set_xlim(-2, 2)
ax2.set_ylim(-1, 1)
ax2.set_aspect('equal')
ax2.axis('off')

def update_bar(angle_deg):
    t = plt.matplotlib.transforms.Affine2D().rotate_deg_around(0, 0, angle_deg) + ax2.transData
    bar.set_transform(t)

def update(frame):
    raw = ser.readline().decode().strip()
    if not raw: return line_pitch, bar
    try:
        pitch = float(raw)
        pitch_buf.append(pitch)
        x_idx.append(len(x_idx) + 1 if x_idx else 1)
        update_bar(pitch)
    except:
        return line_pitch, bar
    line_pitch.set_data(range(len(pitch_buf)), pitch_buf)
    return line_pitch, bar

ani = animation.FuncAnimation(fig, update, interval=30, blit=True)
plt.tight_layout()
plt.show()
