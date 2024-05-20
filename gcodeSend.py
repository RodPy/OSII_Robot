import serial
import time

def conectar_puerto_serial(puerto, baudios=115200):
    try:
        ser = serial.Serial(puerto, baudios, timeout=1)
        print(f"Conectado a {ser.name}")
        return ser
    except serial.SerialException as e:
        print(f"Error al conectar al puerto serial: {e}")
        return None

def send_gcode(ser, gcode):
    try:
        ser.write(gcode.encode('utf-8'))
        print(f"Código G enviado: {gcode}")
        start_time = time.time()
        response = ser.read(ser.in_waiting).decode('utf-8')
        print(f"Respuesta recibida: {response}")
        return response
    except serial.SerialException as e:
        print(f"Error al enviar código G: {e}")
        return None


def cerrar_puerto_serial(ser):
    if ser.is_open:
        ser.close()
        print("Puerto serial cerrado")

if __name__ == "__main__":
    puerto_serial = "COM3"  # Reemplaza con el puerto serial de tu impresora (puede ser "COMx" en Windows o "/dev/ttyUSBx" en Linux)
    serial_port = conectar_puerto_serial(puerto_serial)
    gcode= '$X \n'
    response = send_gcode(serial_port, gcode)
    print(f"Respeusta -> {response}")        # Realizar cualquier procesamiento adicional con la respuesta aquí
    time.sleep(15)
    cerrar_puerto_serial(serial_port)