from datetime import datetime

from gaussmeter_reader import GaussmeterReader
from serialCNC import conectar_puerto_serial,enviar_codigo_g,cerrar_puerto_serial
from database import *
from sphere_path_generator import generate_g_code_for_sphere
import time
from database import Database

def main():
    db = Database(dbname='Ossi_AGOUST_XX', user='postgres', password='admin')
    db.create_table()

    puerto_serial = "COM3"  # Reemplaza con el puerto serial de tu impresora (puede ser "COMx" en Windows o "/dev/ttyUSBx" en Linux)
    baudios = 115200  # Ajusta la velocidad de baudios según la configuración de tu impresora

    serial_port = conectar_puerto_serial(puerto_serial, baudios)

# while True:
    Sensor = GaussmeterReader()
    #
    lectura =Sensor.read_gaussmeter()

    print(f'read_gaussmeter -> {lectura}')
        # print(f'close -> {Sensor.close()}')
        # time.sleep(2)

    radius=120
    step= 10
    speed= 450
    sample_time=2

    print(f'Esfera Radio= {radius} Pasos = {step}')

    g_code=[]

    g_code = generate_g_code_for_sphere()
    c=0
    codigo_g_a_enviar = "$X\n"
    enviar_codigo_g(serial_port, codigo_g_a_enviar)
    time.sleep(sample_time+10)

    codigo_g_a_enviar = "$X\n"
    enviar_codigo_g(serial_port,codigo_g_a_enviar)
    time.sleep(sample_time+10)
    #
    # codigo_g_a_enviar="G10 P0 L20 X0 Y0 Z0 \n"
    # enviar_codigo_g(serial_port,codigo_g_a_enviar)

    codigo_g_a_enviar = f"G10 P0 L20 X0 Y0 Z0\n"
    print(f"origen -> {codigo_g_a_enviar}")
    print(enviar_codigo_g(serial_port, codigo_g_a_enviar))
    time.sleep(sample_time+5)

    codigo_g_a_enviar = f"G21 G17 G90 G1 X0.00 Y0.00 Z-110.00 F400\n"
    print(f'cerca -> {codigo_g_a_enviar}')
    print(enviar_codigo_g(serial_port, codigo_g_a_enviar))
    time.sleep(sample_time+15)

    for X_code,Y_code, Z_code, speed in g_code:
        c+=1
        if serial_port:
            codigo_g_a_enviar = f"G21 G17 G90 G1 X{X_code:.2f} Y{Y_code:.2f} Z{Z_code:.2f} F{speed}\n"
            response = enviar_codigo_g(serial_port, codigo_g_a_enviar)
            print(f'index:{c}/{len(g_code)} Code: {response} X{X_code} Y{Y_code} Z{Z_code} Time aprox: {len(g_code)-c *(sample_time+2)}. ')
            # cerrar_puerto_serial(serial_port)
            time.sleep(sample_time + 2)

            db.insert_data(
                datetime.now().date(),
                # '2024-06-07',
                X_code,
                Y_code,
                Z_code,
                Sensor.read_gaussmeter(),
                Sensor.read_gaussmeter(),
                Sensor.read_gaussmeter(),
                datetime.now().date(),
                # '2024-07-06 12:00:00',
                step
            )

        # db.insert_data(data_to_insert)
            if str(response) == "ok":
                print(
                    f'OK index:{c}/{len(g_code)}) Sensor_X:{Sensor.read_gaussmeter()} '
                )

                time.sleep(sample_time + 5)

                # db.insert_data(
                #     # datetime.now().date(),
                #     '2024-05-07',
                #     X_code,
                #     Y_code,
                #     Z_code,
                #     Sensor.read_gaussmeter(),
                #     Sensor.read_gaussmeter(),
                #     Sensor.read_gaussmeter(),
                #     '2024-05-07 12:00:00',
                #     step
                # )
                continue
    codigo_g_a_enviar = f"G21 G17 G90 G1 X0.00 Y0.00 Z0.00 F400\n"
    print(f'FIN -> {codigo_g_a_enviar}')
    print(enviar_codigo_g(serial_port, codigo_g_a_enviar))
    db.close()

if __name__ == "__main__":
    main()