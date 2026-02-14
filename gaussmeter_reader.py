"""
GaussmeterReader - Comunicación con magnetómetro por puerto serie.
Adaptado por Rodney Rojas desde trabajo de Asiimwe Robert. Version: August 2024 (optimized).
"""
import numbers
import serial
from serial.serialutil import PortNotOpenError
from typing import Union

# Comando hex para solicitar dato (constante evita recrear bytearray en cada lectura)
DATA_COMMAND_HEX = "030000000000"
DATA_RESPONSE_LENGTH = 13
DATA_BYTES_SLICE = slice(6, 12)  # bytes 6..11 para valor y exponente


class GaussmeterReader:
    """
    Lee intensidad de campo magnético (Gauss) desde magnetómetro por puerto serie.
    """

    def __init__(
        self,
        magnetometer_port: str = "COM4",
        baudrate: int = 115200,
        timeout: float = 2.0,
    ) -> None:
        if hasattr(self, "magnetometer") and self.magnetometer.is_open:
            return
        try:
            self.magnetometer = serial.Serial(
                port=magnetometer_port,
                baudrate=baudrate,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=timeout,
            )
        except PortNotOpenError:
            raise PortNotOpenError("Attempting to use a port that is not open")
        except serial.SerialException as e:
            raise serial.SerialException(
                f"Could not open magnetometer port {magnetometer_port}: {e}"
            ) from e

    def read_value(self) -> Union[float, str]:
        """
        Envía comando de dato y lee respuesta.
        :return: Intensidad en Gauss o '' si la respuesta no es válida.
        """
        self.magnetometer.write(bytearray.fromhex(DATA_COMMAND_HEX))
        output_data = self.magnetometer.read(DATA_RESPONSE_LENGTH)

        if len(output_data) != DATA_RESPONSE_LENGTH:
            return ""

        data_bytes = output_data[DATA_BYTES_SLICE]
        raw = (
            (data_bytes[2] << 24)
            | (data_bytes[3] << 16)
            | (data_bytes[4] << 8)
            | data_bytes[5]
        )
        processing_byte = data_bytes[1]
        exponent = processing_byte & 7
        sign = float(1 - 2 * ((processing_byte & 8) >> 3))
        return sign * raw / (10 ** exponent)

    def read_gaussmeter(self, max_retries: int = 100) -> float:
        """
        Lee hasta obtener un valor numérico válido.
        :param max_retries: Límite de intentos para evitar bucle infinito.
        :return: Intensidad en Gauss.
        :raises RuntimeError: Si no se obtiene valor válido tras max_retries.
        """
        for _ in range(max_retries):
            val = self.read_value()
            if isinstance(val, numbers.Number):
                return float(val)
        raise RuntimeError(
            f"Gaussmeter did not return valid value after {max_retries} attempts"
        )

    def close(self) -> None:
        """Cierra el puerto serie del magnetómetro."""
        if getattr(self, "magnetometer", None) and self.magnetometer.is_open:
            self.magnetometer.close()
            print("Magnetometer connection closed.")
