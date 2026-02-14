"""
November 2024 - Version 7.0 (optimized)
Author: Rodney Rojas - Sustainable MRI Lab

main.py
Comunica con CNC por puerto serie, lee sensor Gaussmeter, genera G-code de trayectoria
esférica e inserta datos en PostgreSQL. Optimizado con config centralizada y commits por lotes.
"""
from datetime import datetime
import time

from config import (
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_PORT,
    SERIAL_CNC_PORT,
    SERIAL_GAUSSMETER_PORT,
    SERIAL_BAUD_RATE,
    SPHERE_RADIUS,
    SPHERE_STEP,
    SPHERE_SPEED,
    SAMPLE_TIME_SEC,
)
from database import Database
from gaussmeter_reader import GaussmeterReader
from serialCNC import connect_serial_port, send_g_code, close_serial_port
from sphere_path_generator import generate_g_code_for_sphere

# Tamaño del lote para commit a BD (reduce I/O)
INSERT_BATCH_SIZE = 20


def main() -> None:
    db = Database(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD,
        host=DB_HOST, port=DB_PORT,
    )
    db.create_table()

    serial_port = connect_serial_port(SERIAL_CNC_PORT, SERIAL_BAUD_RATE)
    if serial_port is None:
        print("Error: No se pudo conectar al puerto serie. Abortando.")
        db.close()
        return

    sensor = GaussmeterReader(magnetometer_port=SERIAL_GAUSSMETER_PORT)
    try:
        _run_measurement_loop(db, serial_port, sensor)
    finally:
        db.close()
        close_serial_port(serial_port)
        if hasattr(sensor, "close"):
            sensor.close()


def _run_measurement_loop(
    db: Database,
    serial_port,
    sensor: GaussmeterReader,
) -> None:
    sample_time = SAMPLE_TIME_SEC
    radius = SPHERE_RADIUS
    step = SPHERE_STEP
    speed = SPHERE_SPEED

    reading = sensor.read_gaussmeter()
    print(f"Read Gaussmeter -> {reading}")

    g_code = generate_g_code_for_sphere(radius=radius, step=step, speed=speed)
    total = len(g_code)
    print(f"Sphere Radius = {radius}, Steps = {step}, Points = {total}")

    # Desbloqueo y origen
    send_g_code(serial_port, "$X\n")
    time.sleep(sample_time + 10)

    send_g_code(serial_port, "G10 P0 L20 X0 Y0 Z0\n")
    print("Setting origin -> G10 P0 L20 X0 Y0 Z0")
    time.sleep(sample_time + 5)

    now_date = datetime.now().date()
    now_ts = datetime.now()
    db.insert_data(now_date, 0, 0, 0, sensor.read_gaussmeter(), now_ts, step)

    # Posición inicial
    z_start = 10 - radius
    send_g_code(serial_port, f"G21 G17 G90 G1 X0.00 Y0.00 Z{z_start:.2f} F400\n")
    print(f"Moving to start position -> Z{z_start:.2f}")
    time.sleep(sample_time + 15)

    pending_rows: list = []
    for c, (x_code, y_code, z_code, feed) in enumerate(g_code, 1):
        send_g_code(
            serial_port,
            f"G21 G17 G90 G1 X{x_code:.2f} Y{y_code:.2f} Z{z_code:.2f} F{feed}\n",
        )
        remaining = (total - c) * sample_time
        print(f"Index: {c}/{total} | X:{x_code}, Y:{y_code}, Z:{z_code} | ~{remaining:.0f}s left")

        row = (
            datetime.now().date(),
            x_code, y_code, z_code,
            sensor.read_gaussmeter(),
            datetime.now(),
            step,
        )
        pending_rows.append(row)
        if len(pending_rows) >= INSERT_BATCH_SIZE:
            db.insert_many(pending_rows)
            pending_rows.clear()

    if pending_rows:
        db.insert_many(pending_rows)

    send_g_code(serial_port, "G21 G17 G90 G1 X0.00 Y0.00 Z0.00 F400\n")
    print("FIN -> Return to origin")


if __name__ == "__main__":
    main()
