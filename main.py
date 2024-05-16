from datetime import datetime

from gaussmeter_reader import GaussmeterReader
from serialCNC import conectar_puerto_serial,enviar_codigo_g,cerrar_puerto_serial
from database import *
from sphere_path_generator import generate_g_code_for_sphere
import time
from database import Database

def main():
    db = Database(dbname='osii', user='postgres', password='admin')
    db.create_table()

    puerto_serial = "COM5"  # Reemplaza con el puerto serial de tu impresora (puede ser "COMx" en Windows o "/dev/ttyUSBx" en Linux)
    baudios = 115200  # Ajusta la velocidad de baudios según la configuración de tu impresora

    serial_port = conectar_puerto_serial(puerto_serial, baudios)

# while True:
    Sensor = GaussmeterReader()
    #
    lectura =Sensor.read_gaussmeter()
    # print(f'read_value -> {Sensor.read_value()}')
    print(f'read_gaussmeter -> {lectura}')
        # print(f'close -> {Sensor.close()}')
        # time.sleep(2)

    radius=100
    step= 1
    speed= 100
    sample_time=1

    print(f'Esfera Radio= {radius} Pasos = {step}')

    g_code=[]
    g_code.append()

    g_code = generate_g_code_for_sphere(speep=speed)
    print(type(g_code))
    c=0

    for X_code,Y_code, Z_code, speed in g_code:
        c+=1

        print(f'index:{c}/{len(g_code)}) X{X_code} Y{Y_code} Z{Z_code} Sensor_X:{lectura} Sensor_Y:{lectura} Sensor_Z:{lectura} F{speed}')

        if serial_port:
            codigo_g_a_enviar = f"G21 G17 G90 G1 X{X_code:.2f} Y{Y_code:.2f} Z{Z_code:.2f} F{speed}\n"
            enviar_codigo_g(serial_port, codigo_g_a_enviar)
            cerrar_puerto_serial(serial_port)

        db.insert_data  (
            # datetime.now().date(),
                '2024-05-07',
            X_code,
            Y_code,
            Z_code,
            Sensor.read_gaussmeter(),
            Sensor.read_gaussmeter(),
            Sensor.read_gaussmeter(),
                '2024-05-07 12:00:00',
            step
        )
        # db.insert_data(data_to_insert)
        time.sleep(sample_time)

    db.close()

if __name__ == "__main__":
    main()