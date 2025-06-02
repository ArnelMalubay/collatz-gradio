def get_sequence(n):
    sequence = [n]
    curr = n  
    while curr != 1:
        if curr % 2 == 0:
            curr = curr // 2
        else:
            curr = 3 * curr + 1
        sequence.append(curr)
    sequence.reverse()
    return sequence

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle

# Assume get_sequence is already defined
numbers = get_sequence(100)

# Config
angle_slant = np.pi / 6  # 30 degrees
line_length = 2.5
circle_radius = 1

# Compute margins and starting position based on sequence length
x_margin = len(numbers) * line_length / 2
y_margin = len(numbers) * line_length
start_y = -y_margin / 3

# Set figure size dynamically (figsize in inches)
fig_width = x_margin / 3
fig_height = y_margin / 2
fig, ax = plt.subplots(figsize=(fig_width, fig_height))
ax.set_aspect('equal')
ax.axis('off')

# Set plot limits
ax.set_xlim(-x_margin, x_margin)
ax.set_ylim(start_y, start_y + y_margin + 2)

# Initial position and storage
positions = [(0, circle_radius + start_y + 0.2)]
lines = []
circles = []
texts = []

def update(frame):
    curr_num = numbers[frame]

    if frame == 0:
        pos = positions[0]
    else:
        prev_pos = positions[-1]
        angle = np.pi / 2 - angle_slant if curr_num % 2 else np.pi / 2 + angle_slant
        dx = line_length * np.cos(angle)
        dy = line_length * np.sin(angle)
        pos = (prev_pos[0] + dx, prev_pos[1] + dy)
        positions.append(pos)

        # Draw line
        line = ax.plot([prev_pos[0], pos[0]], [prev_pos[1], pos[1]], 'k-', zorder=1)[0]
        lines.append(line)

    # Draw circle and text
    circle = Circle(pos, circle_radius, edgecolor='black', facecolor='white', zorder=2)
    text = ax.text(pos[0], pos[1], str(curr_num), ha='center', va='center', fontsize=8, zorder=3)
    ax.add_patch(circle)
    circles.append(circle)
    texts.append(text)

    return lines + circles + texts

# Create the animation (stops after showing all elements)
ani = FuncAnimation(
    fig,
    update,
    frames=len(numbers),
    interval=800,
    blit=True,
    repeat=False
)

plt.show()