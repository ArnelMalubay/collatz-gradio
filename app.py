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

# # Assume get_sequence is already defined
# numbers = get_sequence(27)

# # Config
# angle_slant = np.pi / 6  # 30 degrees
# line_length = 2.5
# circle_radius = 1

# # Compute margins and starting position based on sequence length
# x_margin = len(numbers) * line_length / 2
# y_margin = len(numbers) * line_length
# start_y = -y_margin / 3

# # Set figure size dynamically (figsize in inches)
# fig_width = x_margin / 3
# fig_height = y_margin / 2
# fig, ax = plt.subplots(figsize=(fig_width, fig_height))
# ax.set_aspect('equal')
# ax.axis('off')

# # Set plot limits
# ax.set_xlim(-x_margin, x_margin)
# ax.set_ylim(start_y, start_y + y_margin + 2)

# # Initial position and storage
# positions = [(0, circle_radius + start_y + 0.2)]
# lines = []
# circles = []
# texts = []

# def update(frame):
#     curr_num = numbers[frame]

#     if frame == 0:
#         pos = positions[0]
#     else:
#         prev_pos = positions[-1]
#         angle = np.pi / 2 - angle_slant if curr_num % 2 else np.pi / 2 + angle_slant
#         dx = line_length * np.cos(angle)
#         dy = line_length * np.sin(angle)
#         pos = (prev_pos[0] + dx, prev_pos[1] + dy)
#         positions.append(pos)

#         # Draw line
#         line = ax.plot([prev_pos[0], pos[0]], [prev_pos[1], pos[1]], 'k-', zorder=1)[0]
#         lines.append(line)

#     # Draw circle and text
#     circle = Circle(pos, circle_radius, edgecolor='black', facecolor='white', zorder=2)
#     text = ax.text(pos[0], pos[1], str(curr_num), ha='center', va='center', fontsize=8, zorder=3)
#     ax.add_patch(circle)
#     circles.append(circle)
#     texts.append(text)

#     return lines + circles + texts

# # Create the animation (stops after showing all elements)
# ani = FuncAnimation(
#     fig,
#     update,
#     frames=len(numbers),
#     interval=300,
#     blit=True,
#     repeat=False
# )

# plt.show()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Generate branches using your get_sequence function
branches = [get_sequence(i) for i in range(1, 500)]

# Configurable parameters
max_slant_angle = np.pi / 3     # 60 degrees
min_slant_angle = 0    # 15 degrees
line_length = 1.5
animation_interval = 1        # milliseconds
pause_duration = 2              # pause frames between branches

# Shared starting point
start_pos = (0, 0)

# Set up figure
fig, ax = plt.subplots(figsize=(8, 10))
ax.set_aspect('equal')
ax.axis('off')

# Determine dynamic limits
max_steps = max(len(branch) for branch in branches)
x_margin = max_steps * line_length / 4
y_margin = max_steps * line_length / 2
ax.set_xlim(-x_margin, x_margin)
ax.set_ylim(0, y_margin)

# Compute a slant angle per branch
num_branches = len(branches)
slant_angles = np.linspace(max_slant_angle, min_slant_angle, num_branches)

# Track positions and total frames
positions = [[start_pos] for _ in branches]
colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'teal', 'olive']

# Frame schedule per branch
frame_schedule = []
for i, branch in enumerate(branches):
    for j in range(len(branch) - 1):
        frame_schedule.append((i, j))
    frame_schedule += [(-1, -1)] * pause_duration  # Pause after each branch

def update(frame):
    if frame >= len(frame_schedule):
        return []

    branch_idx, step_idx = frame_schedule[frame]
    if branch_idx == -1:
        return []  # pause frame

    branch = branches[branch_idx]
    slant_angle = slant_angles[branch_idx]
    prev_x, prev_y = positions[branch_idx][-1]
    next_val = branch[step_idx + 1]

    # Direction based on parity
    angle = np.pi / 2 + slant_angle if next_val % 2 == 0 else np.pi / 2 - slant_angle
    dx = line_length * np.cos(angle)
    dy = line_length * np.sin(angle)
    new_x, new_y = prev_x + dx, prev_y + dy

    # Draw line segment
    ax.plot(
        [prev_x, new_x], [prev_y, new_y],
        color=colors[branch_idx % len(colors)],
        linewidth=2
    )
    positions[branch_idx].append((new_x, new_y))

    return []

# Animate
ani = FuncAnimation(
    fig,
    update,
    frames=len(frame_schedule),
    interval=animation_interval,
    blit=False,
    repeat=False
)

plt.show()