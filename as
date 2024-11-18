# GaussmeterReader Class
# Adapted by Rodney Rojas from Tom's work
# Purpose: This class handles the communication with a magnetometer via a serial connection.
# It provides functionality to open the serial port, read magnetic field strength values,
# and close the connection to the magnetometer.
# Version: August 2024

import numbers
import serial
from serial.serialutil import PortNotOpenError

class GaussmeterReader:
    """
    GaussmeterReader class for reading data from a magnetometer connected via serial port.
    This class handles opening the serial port, reading magnetic field strength values,
    and closing the connection.
    """

    def __init__(self, magnetometer_port='COM4'):
        """
        Initializes the GaussmeterReader and opens the serial connection.

        :param magnetometer_port: The serial port to which the magnetometer is connected.
        """
        try:
            # If the magnetometer connection is already open, skip reopening it
            if hasattr(self, 'magnetometer') and self.magnetometer.is_open:
                print("Port is already open. Skipping connection.")
                return

            # Open the serial connection for the magnetometer
            self.magnetometer = serial.Serial(
                port=magnetometer_port,
                baudrate=115200,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=2
            )
        except PortNotOpenError:
            raise PortNotOpenError("Attempting to use a port that is not open")

    def read_value(self):
        """
        Sends a data command to the magnetometer and reads the response.

        :return: The magnetic field strength in Gauss or an empty string if the response is invalid.
        """
        dataCommand = '030000000000'
        self.magnetometer.write(bytearray.fromhex(dataCommand))
        outputData = self.magnetometer.read(13)

        if len(outputData) == 13:
            # Extract and process the data from the response
            dataBytes = outputData[6:-1]
            rawDataByte = (dataBytes[2] << 24) | (dataBytes[3] << 16) | (dataBytes[4] << 8) | dataBytes[5]
            processingByte = dataBytes[1]
            exponent = processingByte & 7
            sign = float(1 - 2 * ((processingByte & 8) >> 3))

            # Calculate the magnetic field strength
            fieldStrength = sign * rawDataByte / 10 ** exponent
            return fieldStrength
        return ''  # Return empty string if data is not valid

    def read_gaussmeter(self):
        """
        Continuously reads the Gaussmeter value until a valid number is returned.

        :return: The magnetic field strength in Gauss.
        """
        probeVal = self.read_value()
        while not isinstance(probeVal, numbers.Number):  # Ensure a valid numeric value
            probeVal = self.read_value()
        return probeVal

    def close(self):
        """
        Closes the serial connection to the magnetometer.
        """
        if self.magnetometer.is_open:
            self.magnetometer.close()
            print("Magnetometer connection closed.")








