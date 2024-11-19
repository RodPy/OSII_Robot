"""
November 2024 - Version 6.1
Author: Rodney Rojas - Sustainable MRI Lab  

Description:  
This script communicates with a CNC machine via serial port, reads data from a Gaussmeter sensor,  
and generates G-code for a sphere path. It inserts data into a PostgreSQL database for tracking.  
The CNC machine performs movements based on the generated G-code while the sensor data is recorded.  
"""

from datetime import datetime
from gaussmeter_reader import GaussmeterReader
from serialCNC import connect_serial_port, send_g_code, close_serial_port
from database import Database
from sphere_path_generator import generate_g_code_for_sphere
# from dht_sensor import DHTSensor
import time

def main():
    # Initialize database connection and create table
    db = Database(dbname='Ossi_November_XX', user='postgres', password='admin')
    db.create_table()

    # Serial port and baud rate configuration
    serial_port_name = "COM3"  # Replace with correct serial port (e.g., "COMx" or "/dev/ttyUSBx")
    baud_rate = 115200  # Update according to CNC machine configuration

    # Connect to serial port
    serial_port = connect_serial_port(serial_port_name, baud_rate)

    # Initialize the Gaussmeter sensor
    sensor = GaussmeterReader()

    # Read initial sensor data
    reading = sensor.read_gaussmeter()
    print(f'Read Gaussmeter -> {reading}')

    # Sphere parameters for path generation
    radius = 120
    step = 10
    speed = 450
    sample_time = 2

    print(f'Sphere Radius = {radius}, Steps = {step}')

    # Generate G-code for the sphere path
    g_code = generate_g_code_for_sphere(radius=radius,step=step,speed=speed)

    # Start CNC machine with unlock command
    g_code_to_send = "$X\n"
    send_g_code(serial_port, g_code_to_send)
    time.sleep(sample_time + 10)

    # Reset position
    g_code_to_send = f"G10 P0 L20 X0 Y0 Z0\n"
    print(f"Setting origin -> {g_code_to_send}")
    send_g_code(serial_port, g_code_to_send)
    time.sleep(sample_time + 5)
    # Insert data into the database
    db.insert_data(
        datetime.now().date(),
        0,
        0,
        0,
        sensor.read_gaussmeter(),
        datetime.now().date(),
        step
    )

    # Move to start position
    g_code_to_send = f"G21 G17 G90 G1 X0.00 Y0.00 Z{10-radius} F400\n"
    print(f'Moving to start position -> {g_code_to_send}')
    send_g_code(serial_port, g_code_to_send)
    time.sleep(sample_time + 15)

    # Iterate through generated G-code and send to CNC machine
    for c, (X_code, Y_code, Z_code, speed) in enumerate(g_code, 1):
        g_code_to_send = f"G21 G17 G90 G1 X{X_code:.2f} Y{Y_code:.2f} Z{Z_code:.2f} F{speed}\n"
        response = send_g_code(serial_port, g_code_to_send)
        print(f'Index: {c}/{len(g_code)} | Code Response: {response} | X: {X_code}, Y: {Y_code}, Z: {Z_code}, Approx. Time Remaining: {(len(g_code) - c)*sample_time} seconds')

        # Insert data into the database
        db.insert_data(
            datetime.now().date(),
            X_code,
            Y_code,
            Z_code,
            sensor.read_gaussmeter(),
            datetime.now().date(),
            step
        )

    # End the movement and return to home position
    g_code_to_send = f"G21 G17 G90 G1 X0.00 Y0.00 Z0.00 F400\n"
    print(f'FIN -> {g_code_to_send}')
    send_g_code(serial_port, g_code_to_send)

    # Close the database connection
    db.close()

if __name__ == "__main__":
    main()
