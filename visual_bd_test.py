"""
October 2024
Version: 2.3
Author: Rodney Rojas
Sustainable MRI Lab

visual_db_test.py
Description:
This script generates a real-time 3D visualization of coordinates fetched from a PostgreSQL database.
It plots the coordinates in a 3D space and updates the plot every second.
"""
import psycopg2
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
from database import Database



# Database connection configuration
db = Database(dbname='Ossi_AGOUST_XX', user='postgres', password='admin')

cursor = db.conn.cursor()

# Setting up the 3D plot for visualization
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('X Coordinate')
ax.set_ylabel('Y Coordinate')
ax.set_zlabel('Z Coordinate')

# Lists to store the coordinates
x_coords = []
y_coords = []
z_coords = []

# Function to update the 3D plot with data from the database
def update_graph():
    # Query the database for the coordinates (X, Y, Z)
    cursor.execute("SELECT coordinate_x, coordinate_y, coordinate_z FROM data")
    rows = cursor.fetchall()

    if rows:
        # Clear existing coordinates in the plot
        x_coords.clear()
        y_coords.clear()
        z_coords.clear()

        # Add new coordinates to the respective lists
        for row in rows:
            x_coords.append(row[0])
            y_coords.append(row[1])
            z_coords.append(row[2])

        # Clear the previous plot and update with new data
        ax.clear()
        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')
        ax.set_zlabel('Z Coordinate')
        ax.scatter(x_coords, y_coords, z_coords, c='g', marker='o')
        plt.draw()

# Configure matplotlib for interactive mode
plt.ion()
plt.show()

# Real-time update of the graph
try:
    while True:
        update_graph()  # Fetch and plot new data
        plt.pause(1)    # Pause for 1 second before next update
except KeyboardInterrupt:
    print("Interrupted by user")

# Close the database connection when finished
db.close()
