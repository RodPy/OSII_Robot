import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import imageio


# Definir la clase Database
class Database:
    def __init__(self, dbname, user, password, host='localhost', port='5432'):
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

    def close(self):
        if self.conn:
            self.conn.close()

# Conexión a la base de datos PostgreSQL
db = Database(dbname='osii', user='postgres', password='admin')

try:
    cursor = db.conn.cursor()

    # Paso 2: Extraer los datos
    query = "SELECT coordinate_x, coordinate_y, coordinate_z, x_probe FROM data"
    df = pd.read_sql_query(query, db.conn)

finally:
    # Cerrar el cursor y la conexión
    cursor.close()
    db.close()

# Convertir los datos a arrays de numpy
x = df['coordinate_x'].to_numpy()
y = df['coordinate_y'].to_numpy()
z = df['coordinate_z'].to_numpy()
c = df['x_probe'].to_numpy()

# Crear los frames para la animación
frames = []
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for angle in range(0, 360, 10):
    ax.clear()
    img = ax.scatter(x, y, z, c=c, cmap='hot')
    ax.view_init(30, angle)  # Cambiar el ángulo de la vista
    # Añadir una barra de color
    cbar = fig.colorbar(img)
    cbar.set_label('x_probe')

    # Etiquetas y título
    ax.set_xlabel('coordinate_x')
    ax.set_ylabel('coordinate_y')
    ax.set_zlabel('coordinate_z')
    ax.set_title('Mapa de Calor 3D de x_probe en función de coordinate_x, coordinate_y y coordinate_z')

    plt.draw()

    # Guardar el frame actual como imagen
    filename = f'frame_{angle}.png'
    plt.savefig(filename)
    frames.append(imageio.imread(filename))

# Crear el GIF animado
imageio.mimsave('heatmap_3d.gif', frames, fps=10)

# Eliminar los archivos de frames
# import os
#
# for filename in frames:
#     os.remove(filename)

# Mostrar el GIF animado
from IPython.display import Image

Image(filename='heatmap_3d.gif')
