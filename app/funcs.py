# This module contains functions to generate and visualize the Collatz sequence.

# Importing necessary libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colormaps
import tempfile

# Generate the Collatz sequence for a given n
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

# Draw all branches as a static plot and return the image file path
def plot_collatz_sequence(max_number, slant_angle, fan_angle, colormap, colorperiod):
    
    # Get all sequences
    branches = [get_sequence(i) for i in range(1, max_number + 1)]
    num_branches = len(branches)

    # Convert angles to radians
    slant_angle = np.radians(slant_angle)
    fan_angle = np.radians(fan_angle)
    
    # Set up figure
    fig, ax = plt.subplots(figsize = (8, 10))
    ax.set_aspect('equal')
    ax.axis('off')

    # Set line length and canvas limits
    line_length = 1.5
    max_steps = max(len(branch) for branch in branches)
    x_margin = max_steps * line_length / 4
    y_margin = max_steps * line_length / 2
    ax.set_xlim(-x_margin, x_margin)
    ax.set_ylim(0, y_margin)

    # Slant angles for normal branching
    slant_angles = np.linspace(-slant_angle, slant_angle, num_branches)

    # Fan-out angle for first segment
    fan_angles = np.linspace(-fan_angle, fan_angle, num_branches)

    # Prepare colors from colormap
    num_colors = num_branches // colorperiod
    remainder = num_branches % colorperiod
    base_cmap = colormaps[colormap].resampled(num_colors)
    base_colors = [base_cmap(i) for i in range(num_colors)]
    colors = base_colors * colorperiod
    if remainder > 0:
        colors += [base_cmap(i) for i in range(remainder)]  

    # Draw all branches
    for i, branch in enumerate(branches):
        x, y = 0, 0
        positions = [(x, y)]

        for j in range(len(branch) - 1):
            next_val = branch[j + 1]

            if j == 0:
                angle = np.pi / 2 + fan_angles[i]
            else:
                angle = np.pi / 2 + slant_angles[i] if next_val % 2 == 0 else np.pi / 2 - slant_angles[i]

            dx = line_length * np.cos(angle)
            dy = line_length * np.sin(angle)
            x, y = x + dx, y + dy
            positions.append((x, y))

        xs, ys = zip(*positions)
        ax.plot(xs, ys, color = colors[i], linewidth = 2)

    # Save to temp file
    with tempfile.NamedTemporaryFile(delete = False, suffix = ".png") as tmpfile:
        plt.savefig(tmpfile.name, bbox_inches = 'tight', dpi = 100)
        plt.close(fig)
        return tmpfile.name
