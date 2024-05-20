import time
# import Adafruit_BBIO.GPIO as GPIO
import numbers
import serial
from serial.serialutil import PortNotOpenError


class GaussmeterReader:
    # def __init__(self, magnetometer_port='/dev/ttyUSB0'):
    def __init__(self, magnetometer_port='COM4'):
        try:
            # Check if the port is already open
            if hasattr(self, 'magnetometer') and self.magnetometer.is_open:
                print("Port is already open. Skipping connection.")
                return

            # Open the magnetometer serial connection
            self.magnetometer = serial.Serial(
                port=magnetometer_port,  # Check the correct port for your BBB
                baudrate=115200,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=2
            )
        except PortNotOpenError:
            raise PortNotOpenError("Attempting to use a port that is not open")

    def read_value(self):
        # Read values from the Gaussmeter
        dataCommand = '030000000000'
        self.magnetometer.write(bytearray.fromhex(dataCommand))
        outputData = self.magnetometer.read(13)

        if len(outputData) == 13:
            dataBytes = outputData[6:-1]
            typeByte = dataBytes[0]
            processingByte = dataBytes[1]
            rawDataByte = (dataBytes[2] << 24) | (dataBytes[3] << 16) | (dataBytes[4] << 8) | dataBytes[5]
            exponent = processingByte & 7
            sign = float(1 - 2 * ((processingByte & 8) >> 3))
            fieldStrength = sign * rawDataByte / 10 ** exponent
            return fieldStrength
        else:
            return ''

    def read_gaussmeter(self):
        # Read Gaussmeter values
        probeVal = self.read_value()
        while not (isinstance(probeVal, numbers.Number)):
            probeVal = self.read_value()
        return probeVal

    def close(self):
        # Close the magnetometer serial connection
        self.magnetometer.close()