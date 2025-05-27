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

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

# Set up figure and axis
fig, ax = plt.subplots(figsize=(5, 5))
ax.set_xlim(-2, 2)
ax.set_ylim(0, 3)
ax.set_aspect('equal')
ax.axis('off')

lines = []

# Function to draw a fractal tree branch
def draw_branch(x, y, angle, length, depth):
    if depth == 0:
        return
    x_end = x + length * np.cos(angle)
    y_end = y + length * np.sin(angle)
    line, = ax.plot([x, x_end], [y, y_end], color='green', lw=2)
    lines.append(line)
    draw_branch(x_end, y_end, angle + np.pi / 6, length * 0.6, depth - 1)
    draw_branch(x_end, y_end, angle - np.pi / 6, length * 0.6, depth - 1)

# Animation update function
def update(frame):
    for line in lines:
        line.remove()
    lines.clear()
    sway = np.sin(frame / 10) * np.pi / 18
    draw_branch(0, 0, np.pi / 2 + sway, 1, 2)
    return lines

# Create animation
ani = FuncAnimation(fig, update, frames=60, interval=100, blit=True)

# Save animation as video
output_path = "fractal_tree_depth2.gif"
ani.save(output_path, writer='ffmpeg', fps=10)
plt.close(fig)
output_path
