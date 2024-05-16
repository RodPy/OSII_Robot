import serial
import time

def conectar_puerto_serial(puerto, baudios):
    try:
        ser = serial.Serial(puerto, baudios, timeout=1)
        print(f"Conectado a {ser.name}")
        return ser
    except serial.SerialException as e:
        print(f"Error al conectar al puerto serial: {e}")
        return None

def enviar_codigo_g(ser, codigo_g):
    try:
        ser.write(codigo_g.encode('utf-8'))
        print(f"Código G enviado: {codigo_g}")
    except serial.SerialException as e:
        print(f"Error al enviar código G: {e}")

def cerrar_puerto_serial(ser):
    if ser.is_open:
        ser.close()
        print("Puerto serial cerrado")

if __name__ == "__main__":
    puerto_serial = "COM5"  # Reemplaza con el puerto serial de tu impresora (puede ser "COMx" en Windows o "/dev/ttyUSBx" en Linux)
    baudios = 115200  # Ajusta la velocidad de baudios según la configuración de tu impresora

    serial_port = conectar_puerto_serial(puerto_serial, baudios)

    if serial_port:
        codigo_g_a_enviar = "G28\n"  # Ejemplo de código G (homes all axes)
        enviar_codigo_g(serial_port, codigo_g_a_enviar)

        # Esperar un momento para la respuesta de la impresora (ajusta según sea necesario)
        time.sleep(2)

        cerrar_puerto_serial(serial_port)
