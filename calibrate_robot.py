from datetime import datetime

from serialCNC import conectar_puerto_serial,enviar_codigo_g,cerrar_puerto_serial
from sphere_path_generator import generate_g_code_for_sphere, Calibrate_generate_g_code_for_sphere
import time
#import visual_bd_test

def main():
# ls /dev/tty*
    puerto_serial = "/dev/ttyACM0"
  # Reemplaza con el puerto serial de tu impresora (puede ser "COMx" en Windows o "/dev/ttyUSBx" en Linux)
    baudios = 115200  # Ajusta la velocidad de baudios según la configuración de tu impresora

    serial_port = conectar_puerto_serial(puerto_serial, baudios)

# while True:
    sample_time=7



    g_code=[]

    g_code = Calibrate_generate_g_code_for_sphere()

    c=0
    codigo_g_a_enviar = "$X\n"
    enviar_codigo_g(serial_port, codigo_g_a_enviar)
    time.sleep(sample_time)

    codigo_g_a_enviar = "$X\n"
    time.sleep(sample_time)
    #
    # codigo_g_a_enviar="G10 P0 L20 X0 Y0 Z0 \n"
    # enviar_codigo_g(serial_port,codigo_g_a_enviar)

    codigo_g_a_enviar = f"G10 P0 L20 X0 Y0 Z0\n"
    print(f"origen -> {codigo_g_a_enviar}")
    print(enviar_codigo_g(serial_port, codigo_g_a_enviar))
    print("CENTRAL MESURE")
    time.sleep(sample_time)
    c=0

#     mark = False
    for X_code,Y_code, Z_code, speed in g_code:
        c+=1
    
        if serial_port:
            codigo_g_a_enviar = f"G21 G17 G90 G1 X10 F500\n"
            response = enviar_codigo_g(serial_port, codigo_g_a_enviar)

            time.sleep(2)
            codigo_g_a_enviar = f"G21 G17 G90 G1 X{X_code:.2f} Y{Y_code:.2f} Z{Z_code:.2f} F{speed}\n"
            response = enviar_codigo_g(serial_port, codigo_g_a_enviar)
            print(f'index:{c}/{len(g_code)} APROX: {((len(g_code)-c) * sample_time) /60}  Code: {response} X{X_code} Y{Y_code} Z{Z_code}')
            


        time.sleep(sample_time)
            
    codigo_g_a_enviar = f"G21 G17 G90 G1 X0.00 Y0.00 Z0.00 F400\n"
    print(f'FIN -> {codigo_g_a_enviar}')
    print(enviar_codigo_g(serial_port, codigo_g_a_enviar))
    db.close()

if __name__ == "__main__":
    main()
    

