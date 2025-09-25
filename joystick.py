import serial
import pygame

# -----------------------------
# Initialize Pygame
# -----------------------------
pygame.init()

# -----------------------------
# Window setup
# -----------------------------
WIN_WIDTH, WIN_HEIGHT = 800, 600
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Joystick Control")

# -----------------------------
# Character setup
# -----------------------------
CHARACTER_SIZE = 50
CHARACTER_COLOR = (255, 0, 0)
x, y = WIN_WIDTH // 2, WIN_HEIGHT // 2
CHARACTER_SPEED = 5

# -----------------------------
# Serial setup
# -----------------------------
arduino_serial = serial.Serial('COM5', 9600, timeout=1)

# -----------------------------
# Game loop setup
# -----------------------------
clock = pygame.time.Clock()
running = True

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read joystick data from Arduino
    if arduino_serial.in_waiting > 0:
        try:
            line = arduino_serial.readline().decode().strip()
            print("Raw Data:", line)  # Debugging line
            data = line.split(",")
            if len(data) == 3:
                xValue, yValue, button = map(int, data)

                # Map joystick values to character movement
                if xValue < 400:
                    x -= CHARACTER_SPEED
                elif xValue > 600:
                    x += CHARACTER_SPEED

                if yValue < 400:
                    y -= CHARACTER_SPEED
                elif yValue > 600:
                    y += CHARACTER_SPEED
        except Exception as e:
            print("Error:", e)

    # Draw everything
    win.fill((0, 0, 0))  # Clear screen with black
    pygame.draw.circle(win, CHARACTER_COLOR, (x, y), CHARACTER_SIZE)
    pygame.display.flip()

    # Control frame rate
    clock.tick(30)

# Quit Pygame
pygame.quit()
