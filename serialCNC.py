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

import serial
import time

def enviar_codigo_g2(ser, codigo_g, timeout=15):
    try:
        # Enviar el código G al dispositivo
        ser.write(codigo_g.encode('utf-8'))
        print(f"Código G enviado: {codigo_g}")

        # Esperar una respuesta "ok" del dispositivo
        start_time = time.time()
        while True:
            if ser.in_waiting > 0:
                respuesta = ser.readline().decode('utf-8').strip()
                print(f"Respuesta recibida: {respuesta}")
                if respuesta.lower() == "ok":
                    print("Respuesta 'ok' recibida. Continuando...")
                    return True
            if time.time() - start_time > timeout:
                print("Tiempo de espera agotado. No se recibió respuesta 'ok'.")
                return False
    except serial.SerialException as e:
        print(f"Error al enviar código G: {e}")
        return False


def enviar_codigo_g(ser, codigo_g):
    if codigo_g.strip():
        ser.write(codigo_g.encode('utf-8'))
        time.sleep(1)  # Esperar un momento para obtener la respuesta
        response = ser.read(ser.in_waiting).decode('utf-8')
        return str(response)

def cerrar_puerto_serial(ser):
    if ser.is_open:
        ser.close()
        print("Puerto serial cerrado")
def recibir_datos(ser, num_bytes=100):
    try:
        datos = ser.read(num_bytes)
        if datos:
            print(f"Datos recibidos: {datos.decode('utf-8')}")
        else:
            print("No se recibieron datos")
        return datos
    except serial.SerialException as e:
        print(f"Error al recibir datos: {e}")

        return None
if __name__ == "__main__":
    puerto_serial = "COM3"  # Reemplaza con el puerto serial de tu impresora (puede ser "COMx" en Windows o "/dev/ttyUSBx" en Linux)
    baudios = 115200  # Ajusta la velocidad de baudios según la configuración de tu impresora

    serial_port = conectar_puerto_serial(puerto_serial, baudios)

    if serial_port:
        print("Unlok =")
        enviar_codigo_g(serial_port, "$H\n")
        datos = recibir_datos(serial_port, 128)  # Leer 128 bytes de datos
        print(datos)
        time.sleep(20)
        # print("move =")
        # codigo_g_a_enviar = "G21 G17 G90 G1 X-5.77\n"  # Ejemplo de código G (homes all axes)
        # enviar_codigo_g(serial_port, codigo_g_a_enviar)
        # # datos = recibir_datos(serial_port, 128)  # Leer 128 bytes de datos
        # # print(datos)
        #
        # # Esperar un momento para la respuesta de la impresora (ajusta según sea necesario)
        # time.sleep(10)

        cerrar_puerto_serial(serial_port)
