"""
August 2024 - Version 2.0 (optimized)
Author: Rodney Rojas - Sustainable MRI Lab

serialCNC.py
Comunicación con dispositivo por puerto serie: envío de G-code, lectura de respuesta,
cierre de conexión. Pensado para CNC/impresoras 3D.
"""
import time
from typing import Optional

import serial

DEFAULT_BAUD_RATE = 115200
DEFAULT_TIMEOUT = 1
GCODE_SEND_DELAY = 1.0


def connect_serial_port(
    port: str,
    baud_rate: int = DEFAULT_BAUD_RATE,
    timeout: float = DEFAULT_TIMEOUT,
) -> Optional[serial.Serial]:
    """
    Conecta al puerto serie indicado.
    :return: Objeto Serial o None si falla.
    """
    try:
        ser = serial.Serial(port, baud_rate, timeout=timeout)
        print(f"Connected to {ser.name}")
        return ser
    except serial.SerialException as e:
        print(f"Error connecting to serial port: {e}")
        return None


def send_g_code(ser: Optional[serial.Serial], g_code: str) -> str:
    """
    Envía G-code y lee la respuesta disponible.
    :return: Respuesta del dispositivo o cadena vacía.
    """
    if ser is None or not ser.is_open:
        return ""
    g_code = g_code.strip()
    if not g_code:
        return ""
    try:
        ser.write(g_code.encode("utf-8"))
        if not g_code.endswith("\n"):
            ser.write(b"\n")
        time.sleep(GCODE_SEND_DELAY)
        n = ser.in_waiting
        if n > 0:
            return ser.read(n).decode("utf-8", errors="replace")
    except serial.SerialException as e:
        print(f"Error sending G-code: {e}")
    return ""


def send_g_code_with_confirmation(
    ser: Optional[serial.Serial],
    g_code: str,
    timeout: int = 15,
) -> bool:
    """Envía G-code y espera respuesta 'ok'. Devuelve True si se recibe 'ok'."""
    if ser is None or not ser.is_open:
        return False
    try:
        ser.write(g_code.encode("utf-8"))
        if not g_code.endswith("\n"):
            ser.write(b"\n")
        print(f"G-code sent: {g_code.strip()}")
        deadline = time.time() + timeout
        while time.time() < deadline:
            if ser.in_waiting > 0:
                line = ser.readline().decode("utf-8", errors="replace").strip()
                print(f"Response: {line}")
                if line.lower() == "ok":
                    return True
            time.sleep(0.05)
        print("Timeout: 'ok' response not received.")
        return False
    except serial.SerialException as e:
        print(f"Error sending G-code: {e}")
        return False


def close_serial_port(ser: Optional[serial.Serial]) -> None:
    """Cierra el puerto serie si está abierto."""
    if ser is not None and ser.is_open:
        ser.close()
        print("Serial port closed")


def receive_data(
    ser: Optional[serial.Serial],
    num_bytes: int = 100,
) -> Optional[bytes]:
    """Lee hasta num_bytes del puerto."""
    if ser is None or not ser.is_open:
        return None
    try:
        data = ser.read(num_bytes)
        if data:
            print(f"Data received: {data.decode('utf-8', errors='replace')}")
        return data
    except serial.SerialException as e:
        print(f"Error receiving data: {e}")
        return None


if __name__ == "__main__":
    serial_port = connect_serial_port("COM3", 115200)
    if serial_port:
        send_g_code(serial_port, "$H\n")
        receive_data(serial_port, 128)
        time.sleep(20)
        close_serial_port(serial_port)
