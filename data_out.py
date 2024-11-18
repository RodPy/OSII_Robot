"""
November 2024 - Version 4.0
Author: Rodney Rojas - Sustainable MRI Lab

Description:
This script facilitates the retrieval and visualization of 3D spatial data from a PostgreSQL database.
It connects to the database, extracts the required information, and generates a 3D heatmap scatter plot.
Additionally, it calculates statistics such as max, min, mean, and parts per million (ppm).
Designed for use in MRI research and similar applications.

Requirements:
- psycopg2: For PostgreSQL connection
- pandas: For data manipulation
- matplotlib: For data visualization
- numpy: For numerical operations

Make sure the database contains the required schema and the table 'data' with the necessary columns.
"""

import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


class Database:
    """
    Handles connection and interaction with a PostgreSQL database.
    """
    def __init__(self, dbname, user, password, host='localhost', port='5432'):
        """
        Initializes the database connection.
        :param dbname: Name of the database.
        :param user: Database username.
        :param password: Database password.
        :param host: Host address, defaults to 'localhost'.
        :param port: Port number, defaults to '5432'.
        """
        try:
            self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        except psycopg2.Error as e:
            print(f"Error connecting to database: {e}")
            self.conn = None

    def close(self):
        """
        Closes the database connection.
        """
        if self.conn:
            self.conn.close()

dbname='Ossi_04_11_2024_Y_FULL_SHIM_D22_CENTER'
# Step 1: Connect to PostgreSQL database
db = Database(dbname=dbname, user='postgres', password='admin')

try:
    # Create a cursor for executing queries
    cursor = db.conn.cursor()

    # Step 2: Retrieve data from the database
    query = """
    SELECT date, temperature_c, humidity, coordinate_x, coordinate_y, coordinate_z, y_probe
    FROM data
    """
    df = pd.read_sql_query(query, db.conn)

    # Export data to CSV for external analysis or backup
    output_file = dbname
    df.to_csv(output_file, index=False)
    print(f"Data exported to output_{output_file}.csv")

finally:
    # Ensure resources are closed
    if cursor:
        cursor.close()
    db.close()

# Step 3: Generate 3D heatmap
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Convert data to numpy arrays for plotting
x = df['coordinate_x'].to_numpy()
y = df['coordinate_y'].to_numpy()
z = df['coordinate_z'].to_numpy()
c = df['y_probe'].to_numpy()

# Create the scatter plot
scatter = ax.scatter(x, y, z, c=c, cmap='hot')

# Add a color bar for the y_probe values
cbar = fig.colorbar(scatter)
cbar.set_label('Y Probe')

# Add labels and title
ax.set_xlabel('X Coordinate')
ax.set_ylabel('Y Coordinate')
ax.set_zlabel('Z Coordinate')
ax.set_title('3D Heatmap of Y_PROBE')

# Calculate statistics
max_val = df['y_probe'].max()
min_val = df['y_probe'].min()
mean_val = df['y_probe'].mean()
center = 436
ppm = ((max_val - min_val) / mean_val) * 1_000_000

# Print statistics
print(f"Max: {max_val:.2f} - Min: {min_val:.2f} - Mean: {mean_val:.2f} - Center: {center} - PPM: {ppm:.2f}")

# Display the plot
plt.show()
