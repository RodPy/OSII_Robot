"""
October 2024
Version: 2.3
Author: Rodney Rojas
Sustainable MRI Lab

sphere_path_generator.py
Description:
This script generates G-code to create a 3D representation of a sphere using additive manufacturing or CNC tools.
It includes functionality to visualize the sphere and simulate the cutting path. Additionally, it calculates the
estimated time required to complete the trajectory. The G-code is written to a file, and a graphical representation
is provided for validation and analysis.
"""

import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


# Function to generate G-code for a sphere
def generate_g_code_for_sphere(radius=120, step=10, file_out='sphere_gcode.gcode', speed=450):
    """
    Generates G-code for a sphere and saves it to a file.

    Parameters:
        radius (int): Radius of the sphere in mm.
        step (int): Step size for layer height in mm.
        file_out (str): Name of the output G-code file.
        speed (int): Feed rate for the machine in mm/min.

    Returns:
        list: A list of points (x, y, z, speed) representing the sphere's trajectory.
    """
    with open(file_out, 'w') as archivo:
        g_code = []

        # Iterate through each layer of the sphere
        for z in range(-radius, radius + 1, step):
            # Calculate the radius of the circular cross-section at this height
            current_radius = round(math.sqrt(radius ** 2 - z ** 2), 2)

            # Calculate the angular step, ensuring a minimum of 1 degree
            step_angle = max(1, int((step / (0.1 + current_radius)) * (180 / math.pi)))

            # Generate points along the circumference
            for theta in range(0, 360, step_angle):
                x = round(current_radius * math.cos(math.radians(theta)), 2)
                y = round(current_radius * math.sin(math.radians(theta)), 2)
                g_code.append((x, y, z, speed))
                archivo.write(f"G1 X{x:.2f} Y{y:.2f} Z{z:.2f} F{speed}\n")

        archivo.write("M30\n")  # End of program
    return g_code


# Function to plot the sphere and its generated G-code points
def plot_sphere_with_g_code(radius, step):
    """
    Plots the 3D sphere along with the points generated from the G-code.

    Parameters:
        radius (int): Radius of the sphere in mm.
        step (int): Step size for layer height in mm.
    """
    g_code = generate_g_code_for_sphere(radius, step)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the surface of the sphere
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = radius * np.outer(np.cos(u), np.sin(v))
    y = radius * np.outer(np.sin(u), np.sin(v))
    z = radius * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x, y, z, color='b', alpha=0.5)

    # Plot the cutting path points
    for i in range(len(g_code) - 1):
        ax.plot([g_code[i][0], g_code[i + 1][0]],
                [g_code[i][1], g_code[i + 1][1]],
                [g_code[i][2], g_code[i + 1][2]], color='y')

    ax.set_xlim([-radius, radius])
    ax.set_ylim([-radius, radius])
    ax.set_zlim([-radius, radius])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()
