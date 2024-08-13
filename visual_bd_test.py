import psycopg2
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
from database import Database

def plot():
    # Conexión a la base de datos PostgreSQL
    db = Database(dbname='OssiAGOSTO_YY_SHIM', user='postgres', password='admin')

    cursor = db.conn.cursor()

    # Configurar la figura para el gráfico 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_zlabel('Z Coordinate')

    # Inicializar listas para las coordenadas
    x_coords = []
    y_coords = []
    z_coords = []


    # Función para actualizar el gráfico
    def update_graph():
        cursor.execute("SELECT coordinate_x, coordinate_y, coordinate_z FROM data")
        rows = cursor.fetchall()

        if rows:
            x_coords.clear()
            y_coords.clear()
            z_coords.clear()

            for row in rows:
                x_coords.append(row[0])
                y_coords.append(row[1])
                z_coords.append(row[2])

            ax.clear()
            ax.set_xlabel('X Coordinate')
            ax.set_ylabel('Y Coordinate')
            ax.set_zlabel('Z Coordinate')
            ax.scatter(x_coords, y_coords, z_coords, c='g', marker='o')
            plt.draw()


    # Configurar la ventana de matplotlib
    plt.ion()
    plt.show()

    # Actualizar el gráfico en tiempo real
    try:
        while True:
            update_graph()
            plt.pause(1)  # Pausa de 1 segundo antes de la siguiente actualización
    except KeyboardInterrupt:
        print("Interrupción por el usuario")

    # Cerrar la conexión a la base de datos
    db.close()


plot()