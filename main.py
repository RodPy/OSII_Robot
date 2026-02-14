"""
main.py
Aplicación principal: control CNC, gaussmeter, sensor DHT, generación de trayectoria esférica y registro en base de datos.
Main application: CNC control, gaussmeter, DHT sensor, spherical path generation and database logging.
Author: Rodney Rojas
Sustainable MRI Lab
February 2026
Version: 1.0
"""
from datetime import datetime

from gaussmeter_reader import GaussmeterReader
from serialCNC import conectar_puerto_serial,enviar_codigo_g,cerrar_puerto_serial
from database import *
from sphere_path_generator import generate_g_code_for_sphere
import time
from database import Database
from dht_sensor import DHTSensor
#import visual_bd_test

bd = 'Ossi_26_11_2024_Y_FULL_SHIM_D25_CENTER'
def main():
    db = Database(dbname=bd, user='postgres', password='admin')
    db.create_table()
# ls /dev/tty*
    puerto_serial = "/dev/ttyACM0"  # Reemplaza con el puerto serial de tu impresora (puede ser "COMx" en Windows o "/dev/ttyUSBx" en Linux)
    baudios = 115200  # Ajusta la velocidad de baudios según la configuración de tu impresora

    serial_port = conectar_puerto_serial(puerto_serial, baudios)
    # visual_bd_test.plot(bd)

# while True:
    dht_sensor = DHTSensor()
    Sensor = GaussmeterReader()
    #
    lectura =Sensor.read_gaussmeter()
    
   
    try:
        temperature_c, humidity = dht_sensor.read_sensor()
    except Exception as e:
        print(f"Error al leer el sensor: {e}")
        temperature_c = 0
        humidity = 0
    print(f" T= {temperature_c}, H={humidity}")
    print(f'read_gaussmeter -> {lectura}')
        # print(f'close -> {Sensor.close()}')
        # time.sleep(2)

    radius=110
    step= 10
    speed= 450
    sample_time=7

    print(f'Esfera Radio= {radius} Pasos = {step}')

    g_code=[]

    g_code = generate_g_code_for_sphere(radius=radius, step=step, speed=speed)
    c=0
    codigo_g_a_enviar = "$X\n"
    enviar_codigo_g(serial_port, codigo_g_a_enviar)
    time.sleep(sample_time)

    codigo_g_a_enviar = "$X\n"
    enviar_codigo_g(serial_port,codigo_g_a_enviar)
    time.sleep(sample_time)
    #
    # codigo_g_a_enviar="G10 P0 L20 X0 Y0 Z0 \n"
    # enviar_codigo_g(serial_port,codigo_g_a_enviar)

    codigo_g_a_enviar = f"G10 P0 L20 X0 Y0 Z0\n"
    print(f"origen -> {codigo_g_a_enviar}")
    print(enviar_codigo_g(serial_port, codigo_g_a_enviar))
    print("CENTRAL MESURE")
    time.sleep(sample_time)
    
    for i in range(3):
        print(f"Read_Gasusmeter {i} -> {Sensor.read_gaussmeter()}")
        db.insert_data(
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),                # '2024-06-07',
                    temperature_c,
                    humidity,
                    0,
                    0,
                    0,
                    Sensor.read_gaussmeter(),
                    Sensor.read_gaussmeter(),
                    Sensor.read_gaussmeter(),
                    datetime.now().date(),
                    # '2024-07-06 12:00:00',
                    step
                )
        time.sleep(1)


    codigo_g_a_enviar = f"G21 G17 G90 G1 X0.00 Y0.00 Z-90.00 F400\n"
    print(f'cerca -> {codigo_g_a_enviar}')
    print(enviar_codigo_g(serial_port, codigo_g_a_enviar))
    time.sleep(sample_time+10)
#     mark = False
    for X_code,Y_code, Z_code, speed in g_code:
        c+=1
    
        try:
            temperature_c, humidity = dht_sensor.read_sensor()

        except Exception as e:
            print(f"Error al leer el sensor: {e}")
            temperature_c = 0
            humidity = 0
        print(f" T= {temperature_c}, H={humidity}")
    
        if serial_port:
            codigo_g_a_enviar = f"G21 G17 G90 G1 X{X_code:.2f} Y{Y_code:.2f} Z{Z_code:.2f} F{speed}\n"
            response = enviar_codigo_g(serial_port, codigo_g_a_enviar)
            print(f'index:{c}/{len(g_code)} APROX: {((len(g_code)-c) * sample_time) /60}min M: {Sensor.read_gaussmeter()} Code: {response} X{X_code} Y{Y_code} Z{Z_code}')
            # cerrar_puerto_serial(serial_port)
            
#             if (mark):
#                 time.sleep(sample_time + 15)
#                 print("CENTRO_PAUSA")
#                 mark = False
#             
#             if (X_code==0 and Y_code==0 and Z_code==0 ):
#                 time.sleep(sample_time + 15)
#                 print("CENTRO")
#                 mark=True 
#             else:
#                 time.sleep(sample_time)
#                 mark = False
            time.sleep(sample_time)
            for i in range(3):
                print(f"Read_Gasusmeter {i} -> {Sensor.read_gaussmeter()}")

                db.insert_data(
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),                # '2024-06-07',
                    temperature_c,
                    humidity,
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
                time.sleep(1)

            # db.insert_data(data_to_insert)
            # if str(response) == "ok":
            #     print(
            #         f'OK index:{c}/{len(g_code)}) Sensor_X:{Sensor.read_gaussmeter()} '
            #     )

            #     time.sleep(sample_time + 5)

            #     # db.insert_data(
            #     #     # datetime.now().date(),
            #     #     '2024-05-07',
            #     #     X_code,
            #     #     Y_code,
            #     #     Z_code,
            #     #     Sensor.read_gaussmeter(),
            #     #     Sensor.read_gaussmeter(),
            #     #     Sensor.read_gaussmeter(),
            #     #     '2024-05-07 12:00:00',
            #     #     step
            #     # )
            #     continue
    codigo_g_a_enviar = f"G21 G17 G90 G1 X0.00 Y0.00 Z0.00 F400\n"
    print(f'FIN -> {codigo_g_a_enviar}')
    print(enviar_codigo_g(serial_port, codigo_g_a_enviar))
    if serial_port:
        cerrar_puerto_serial(serial_port)
    db.close()

if __name__ == "__main__":
    main()
    

