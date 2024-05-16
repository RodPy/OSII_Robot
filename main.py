from datetime import datetime

from gaussmeter_reader import GaussmeterReader
from database import *
from sphere_path_generator import generate_g_code_for_sphere
import time
from database import Database

def main():
    db = Database(dbname='osii', user='postgres', password='admin')
    db.create_table()


# while True:
    Sensor = GaussmeterReader()
    #
    print(f'read_value -> {Sensor.read_value()}')
    print(f'read_gaussmeter -> {Sensor.read_gaussmeter()}')
        # print(f'close -> {Sensor.close()}')
        # time.sleep(2)

    radius=20
    step= 1
    sample_time=1
    print(f'Esfera Radio= {radius} Pasos = {step}')

    g_code=[]
    g_code.append()

    g_code = generate_g_code_for_sphere(radius, step)
    print(type(g_code))
    c=0
    for X_code,Y_code, Z_code in g_code:
        c+=1
        print(f'index:{c}/{len(g_code)}) X{X_code} Y{Y_code} Z{Z_code} Sensor_X:{Sensor.read_gaussmeter()} Sensor_Y:{Sensor.read_gaussmeter()} Sensor_Z:{Sensor.read_gaussmeter()} F400' )
        time.sleep(sample_time)

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
    db.close()

if __name__ == "__main__":
    main()