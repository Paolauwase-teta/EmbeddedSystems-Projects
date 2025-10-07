import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from collections import deque
import numpy as np

# ----- CONFIG -----
PORT = 'COM3'  # Windows example
BAUD = 115200
WINDOW = 200  # Number of samples

ser = serial.Serial(PORT, BAUD, timeout=1)

pitch_buf = deque(maxlen=WINDOW)
roll_buf = deque(maxlen=WINDOW)
yaw_buf = deque(maxlen=WINDOW)
x_idx = deque(maxlen=WINDOW)

# ----- FIGURE -----
fig = plt.figure(figsize=(10, 8))

# 2D Time-series plot
ax1 = fig.add_subplot(2, 1, 1)
line_pitch, = ax1.plot([], [], label="Pitch", color='blue', linewidth=2)
line_roll, = ax1.plot([], [], label="Roll", color='green', linewidth=2)
line_yaw, = ax1.plot([], [], label="Yaw", color='red', linewidth=2)
ax1.set_xlim(0, WINDOW)
ax1.set_ylim(-180, 180)
ax1.set_ylabel("Angle (°)")
ax1.set_xlabel("Samples")
ax1.legend()
ax1.set_title("MPU6050 Angles over Time")
ax1.grid(True)

# 3D orientation plot
ax2 = fig.add_subplot(2, 1, 2, projection='3d')
ax2.set_xlim([-1.5, 1.5]);
ax2.set_ylim([-1.5, 1.5]);
ax2.set_zlim([-1.5, 1.5])
ax2.set_xlabel('X (Roll)')
ax2.set_ylabel('Y (Pitch)')
ax2.set_zlabel('Z (Yaw)')
ax2.set_title("3D Orientation Cube")

# Define a cube
cube_definition = np.array([[-0.5, -0.5, -0.5],
                            [-0.5, -0.5, 0.5],
                            [-0.5, 0.5, -0.5],
                            [-0.5, 0.5, 0.5],
                            [0.5, -0.5, -0.5],
                            [0.5, -0.5, 0.5],
                            [0.5, 0.5, -0.5],
                            [0.5, 0.5, 0.5]])

# Cube edges (pairs of vertex indices)
edges = [(0, 1), (0, 2), (0, 4), (1, 3), (1, 5), (2, 3), (2, 6),
         (3, 7), (4, 5), (4, 6), (5, 7), (6, 7)]


def parse_line(line):
    try:
        parts = line.strip().split(',')
        if len(parts) != 3:
            return None, None, None
        return float(parts[0]), float(parts[1]), float(parts[2])
    except:
        return None, None, None


def rotation_matrix(pitch, roll, yaw):
    """Returns combined rotation matrix for pitch, roll, yaw in degrees."""
    pitch = np.radians(pitch)
    roll = np.radians(roll)
    yaw = np.radians(yaw)

    Rx = np.array([[1, 0, 0],
                   [0, np.cos(roll), -np.sin(roll)],
                   [0, np.sin(roll), np.cos(roll)]])

    Ry = np.array([[np.cos(pitch), 0, np.sin(pitch)],
                   [0, 1, 0],
                   [-np.sin(pitch), 0, np.cos(pitch)]])

    Rz = np.array([[np.cos(yaw), -np.sin(yaw), 0],
                   [np.sin(yaw), np.cos(yaw), 0],
                   [0, 0, 1]])

    return Rz @ Ry @ Rx


def init():
    line_pitch.set_data([], [])
    line_roll.set_data([], [])
    line_yaw.set_data([], [])
    return line_pitch, line_roll, line_yaw


def update(frame):
    # Read serial lines
    for _ in range(5):
        raw = ser.readline().decode(errors='ignore')
        if not raw: break
        pitch, roll, yaw = parse_line(raw)
        if pitch is None: continue
        pitch_buf.append(pitch)
        roll_buf.append(roll)
        yaw_buf.append(yaw)
        x_idx.append(len(x_idx) + 1 if x_idx else 1)

    # Update 2D lines
    xs = list(range(len(x_idx)))
    line_pitch.set_data(xs, list(pitch_buf))
    line_roll.set_data(xs, list(roll_buf))
    line_yaw.set_data(xs, list(yaw_buf))
    ax1.set_xlim(max(0, len(xs) - WINDOW), max(WINDOW, len(xs)))

    # Update 3D cube
    ax2.cla()
    ax2.set_xlim([-1.5, 1.5]);
    ax2.set_ylim([-1.5, 1.5]);
    ax2.set_zlim([-1.5, 1.5])
    ax2.set_xlabel('X (Roll)');
    ax2.set_ylabel('Y (Pitch)');
    ax2.set_zlabel('Z (Yaw)')
    ax2.set_title("3D Orientation Cube")

    if pitch_buf:
        R = rotation_matrix(pitch_buf[-1], roll_buf[-1], yaw_buf[-1])
        rotated = cube_definition @ R.T
        # Draw edges
        for e in edges:
            ax2.plot([rotated[e[0], 0], rotated[e[1], 0]],
                     [rotated[e[0], 1], rotated[e[1], 1]],
                     [rotated[e[0], 2], rotated[e[1], 2]],
                     color='black', linewidth=2)

    return line_pitch, line_roll, line_yaw


ani = FuncAnimation(fig, update, init_func=init, interval=30, blit=False)
plt.tight_layout()
plt.show()
