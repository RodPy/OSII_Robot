import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Definir la clase Database (asegúrate de tener esta clase definida y accesible)
class Database:
    def __init__(self, dbname, user, password, host='localhost', port='5432'):
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

    def close(self):
        if self.conn:
            self.conn.close()

# Conexión a la base de datos PostgreSQL
db = Database(dbname='OssIJune_GZ', user='postgres', password='admin')

try:
    cursor = db.conn.cursor()

    # Paso 2: Extraer los datos
    query = "SELECT coordinate_x, coordinate_y, coordinate_z, y_probe FROM data"
    df = pd.read_sql_query(query, db.conn)

finally:
    # Cerrar el cursor y la conexión
    cursor.close()
    db.close()

# Paso 3: Crear el mapa de calor en 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Convertir los datos a arrays de numpy
y = df['coordinate_x'].to_numpy()
x = df['coordinate_y'].to_numpy()
z = df['coordinate_z'].to_numpy()
c = df['y_probe'].to_numpy()

# Crear el scatter plot 3D
img = ax.scatter(x, y, z, c=c, cmap='hot')

# Añadir una barra de color
cbar = fig.colorbar(img)
cbar.set_label('y_probe')

# Etiquetas y título
ax.set_xlabel('coordinate_x')
ax.set_ylabel('coordinate_y')
ax.set_zlabel('coordinate_z')
ax.set_title('Heatmap 3D de Y_PROBE')


max= df['y_probe'].max()
min= df['y_probe'].min()
prom = df['y_probe'].mean()
center = 436
ppm = ((max-min)/prom)*1000000

print(f"Max: {max} - Min: {min} - prom: {prom} - center={center} - ppm: {ppm}  ")

plt.show()
