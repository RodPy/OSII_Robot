import psycopg2
import csv


# Función para cargar datos desde un archivo CSV a la base de datos
def cargar_datos_desde_csv(archivo_csv, tabla):
    try:
        # Establecer la conexión con la base de datos

        conn = psycopg2.connect(
            dbname="osii2",
            user="postgres",
            password="admin",
            host="localhost",
            port="5432"
        )
        conn.autocommit = True  # Establecer autocommit en True para que los cambios se apliquen inmediatamente

        # Crear un cursor
        cur = conn.cursor()
        cur.execute("CREATE DATABASE osii2")

        cur.execute("""
                    CREATE TABLE IF NOT EXISTS personas (
                        nombre TEXT,
                        apellido TEXT,
                        edad INTEGER
                    )
                """)
        conn.commit()
        print("Tabla personas creada exitosamente.")

        # Leer el archivo CSV y cargar los datos en la tabla
        with open(archivo_csv, 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            next(reader)  # Saltar la fila de encabezado si la hay
            for row in reader:
                cur.execute("INSERT INTO {} (nombre, apellido, edad) VALUES (%s, %s, %s)".format(tabla), row)

        # Confirmar la transacción
        conn.commit()
        print("Datos insertados exitosamente.")

    except (psycopg2.Error, csv.Error) as e:
        print("Error:", e)
        conn.rollback()

    finally:
        # Cerrar el cursor y la conexión
        # Cerrar el cursor y la conexión
        if cur:
            cur.close()
        if conn:
            conn.close()


# Llamar a la función para cargar datos desde el archivo CSV a la tabla personas
cargar_datos_desde_csv('datos.csv', 'personas')
