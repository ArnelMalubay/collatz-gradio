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
from matplotlib import colormaps

# Assume get_sequence is defined externally
branches = [get_sequence(i) for i in range(1, 101)]

# Configurable parameters
num_simultaneous = 5  # Number of branches to animate simultaneously
max_slant_angle = np.pi / 2     # 60 degrees
min_slant_angle = np.pi / 3             # 0 degrees
line_length = 1.5
animation_interval = 0.1          # milliseconds
pause_duration = 1              # pause frames between branch groups

# Shared starting point
start_pos = (0, 0)

# Set up figure
fig, ax = plt.subplots(figsize=(8, 10))
ax.set_aspect('equal')
ax.axis('off')

# Determine dynamic limits based on all branches
max_steps = max(len(branch) for branch in branches)
x_margin = max_steps * line_length / 4
y_margin = max_steps * line_length / 2
ax.set_xlim(-x_margin, x_margin)
ax.set_ylim(0, y_margin)

# Total branches
num_branches = len(branches)

# Compute slant angles per branch
slant_angles = np.linspace(max_slant_angle, min_slant_angle, num_branches)

# Prepare positions for each branch
positions = [[start_pos] for _ in branches]

# === Color setup ===
# Get base colormap with 20 distinct colors
base_cmap = colormaps['Set1'].resampled(20)
colors_pool = [base_cmap(i) for i in range(20)]

# Pick num_simultaneous colors evenly spaced from the 20-color pool
indices = np.linspace(0, 19, num_simultaneous, dtype=int)
colors = [colors_pool[i] for i in indices]

# Shuffle colors for maximal contrast (zig-zag from ends)
shuffled_colors = []
left, right = 0, num_simultaneous - 1
toggle = True
while left <= right:
    if toggle:
        shuffled_colors.append(colors[left])
        left += 1
    else:
        shuffled_colors.append(colors[right])
        right -= 1
    toggle = not toggle

# === Frame schedule generation ===
frame_schedule = []
for group_start in range(0, num_branches, num_simultaneous):
    group_end = min(group_start + num_simultaneous, num_branches)
    # For all branches in this group
    max_branch_len = max(len(branches[i]) for i in range(group_start, group_end))
    # For each step in branches in group
    for step_idx in range(max_branch_len - 1):
        for branch_idx in range(group_start, group_end):
            branch = branches[branch_idx]
            if step_idx < len(branch) - 1:
                frame_schedule.append((branch_idx, step_idx))
    # Pause after each group
    frame_schedule += [(-1, -1)] * pause_duration

def update(frame):
    if frame >= len(frame_schedule):
        return []

    branch_idx, step_idx = frame_schedule[frame]
    if branch_idx == -1:
        return []  # Pause frame, no drawing

    branch = branches[branch_idx]
    slant_angle = slant_angles[branch_idx]
    prev_x, prev_y = positions[branch_idx][-1]
    next_val = branch[step_idx + 1]

    # Direction based on parity: even = slant left, odd = slant right
    angle = np.pi / 2 + slant_angle if next_val % 2 == 0 else np.pi / 2 - slant_angle
    dx = line_length * np.cos(angle)
    dy = line_length * np.sin(angle)
    new_x, new_y = prev_x + dx, prev_y + dy

    # Draw line segment
    color_idx = branch_idx % num_simultaneous
    color = shuffled_colors[color_idx]
    ax.plot([prev_x, new_x], [prev_y, new_y], color=color, linewidth=2)

    # Save new position
    positions[branch_idx].append((new_x, new_y))

    return []

# Create animation
ani = FuncAnimation(
    fig,
    update,
    frames=len(frame_schedule),
    interval=animation_interval,
    blit=False,
    repeat=False
)

plt.show()
