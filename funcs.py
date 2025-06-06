# This module contains functions to generate and visualize the Collatz sequence.

# Importing necessary libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from matplotlib import colormaps
import tempfile

# This function generates the Collatz sequence for a given integer n. Results are reversed to start from 1 and end in n.
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

# This function creates an animation of the Collatz sequence branches and returns the file path to the saved animation.
def animate_collatz_sequence(max_number = 1000, num_simultaneous = 50, max_slant_angle = 60, min_slant_angle = 5, colormap = 'Set1'):
    
    # Get the Collatz sequences for numbers from 1 to max_number
    branches = [get_sequence(i) for i in range(1, max_number + 1)]

    # Convert angles from degrees to radians    
    max_slant_angle = np.radians(max_slant_angle)
    min_slant_angle = np.radians(min_slant_angle)
    
    # Set up figure
    fig, ax = plt.subplots(figsize = (8, 10))
    ax.set_aspect('equal')
    ax.axis('off')

    # Determine dynamic limits based on all branches
    line_length = 1.5
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
    positions = [[(0, 0)] for _ in branches]

    # Color setup
    base_cmap = colormaps[colormap].resampled(20)
    colors_pool = [base_cmap(i) for i in range(20)]
    
    indices = np.linspace(0, 19, num_simultaneous, dtype = int)
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

    # Frame schedule generation
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
        frame_schedule += [(-1, -1)] * 0.1

    # This helper function updates the plot for each frame in the animation.
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
        ax.plot([prev_x, new_x], [prev_y, new_y], color = color, linewidth = 2)

        # Save new position
        positions[branch_idx].append((new_x, new_y))

        return []

    # Create animation
    ani = FuncAnimation(
        fig,
        update,
        frames = len(frame_schedule),
        interval = 0.1,
        blit = False,
        repeat = False
    )         

    temp_video = tempfile.NamedTemporaryFile(suffix = ".mp4", delete = False)
    writer = FFMpegWriter(fps = 45, bitrate = 1800)

    ani.save(temp_video.name, writer = writer)
    plt.close(fig) 

    return temp_video.name