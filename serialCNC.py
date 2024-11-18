"""
August 2024 - Version 1.5
Author: Rodney Rojas - Sustainable MRI Lab

Description:
This script facilitates communication with a device via a serial port.
It includes functions to send G-code commands, receive responses, and manage the serial connection.
Designed for devices such as 3D printers or CNC controllers.
"""

import serial
import time

def connect_serial_port(port, baud_rate=115200):
    """
    Establishes a connection to the specified serial port.

    Parameters:
        port (str): Serial port (e.g., "COM3" or "/dev/ttyUSB0").
        baud_rate (int): Communication speed in baud.

    Returns:
        serial.Serial: Serial port object if the connection is successful, None otherwise.
    """
    try:
        ser = serial.Serial(port, baud_rate, timeout=1)
        print(f"Connected to {ser.name}")
        return ser
    except serial.SerialException as e:
        print(f"Error connecting to serial port: {e}")
        return None

def send_g_code_with_confirmation(ser, g_code, timeout=15):
    """
    Sends G-code to the connected device and waits for an "ok" response.

    Parameters:
        ser (serial.Serial): Serial port object.
        g_code (str): G-code command to send.
        timeout (int): Maximum time to wait for a response in seconds.

    Returns:
        bool: True if "ok" is received, False otherwise.
    """
    try:
        ser.write(g_code.encode('utf-8'))
        print(f"G-code sent: {g_code}")

        start_time = time.time()
        while True:
            if ser.in_waiting > 0:
                response = ser.readline().decode('utf-8').strip()
                print(f"Response: {response}")
                if response.lower() == "ok":
                    return True
            if time.time() - start_time > timeout:
                print("Timeout: 'ok' response not received.")
                return False
    except serial.SerialException as e:
        print(f"Error sending G-code: {e}")
        return False

def send_g_code(ser, g_code):
    """
    Sends G-code to the connected device and reads the response.

    Parameters:
        ser (serial.Serial): Serial port object.
        g_code (str): G-code command to send.

    Returns:
        str: Response from the device.
    """
    if g_code.strip():
        ser.write(g_code.encode('utf-8'))
        time.sleep(1)
        return ser.read(ser.in_waiting).decode('utf-8')

def close_serial_port(ser):
    """
    Closes the serial port connection.

    Parameters:
        ser (serial.Serial): Serial port object.
    """
    if ser.is_open:
        ser.close()
        print("Serial port closed")

def receive_data(ser, num_bytes=100):
    """
    Reads data from the serial port.

    Parameters:
        ser (serial.Serial): Serial port object.
        num_bytes (int): Number of bytes to read.

    Returns:
        bytes: Received data.
    """
    try:
        data = ser.read(num_bytes)
        if data:
            print(f"Data received: {data.decode('utf-8')}")
        return data
    except serial.SerialException as e:
        print(f"Error receiving data: {e}")
        return None

if __name__ == "__main__":
    serial_port_name = "COM3"  # Replace with the correct port
    baud_rate = 115200         # Update according to device configuration

    serial_port = connect_serial_port(serial_port_name, baud_rate)

    if serial_port:
        send_g_code(serial_port, "$H\n")  # Example unlock command
        received_data = receive_data(serial_port, 128)  # Read 128 bytes
        print(received_data)

        time.sleep(20)
        close_serial_port(serial_port)
