import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math

def generar_puntos_para_cilindro_perpendicular(diametro, altura, pasos=100, niveles=10):
    puntos = []

    # Generar los puntos para cada nivel del cilindro
    for i in range(niveles):
        z = i * altura / (niveles - 1)  # Distribuir los niveles uniformemente a lo largo del eje Z
        for j in range(pasos):
            angulo = j * (2 * math.pi / pasos)
            x = diametro / 2 * math.cos(angulo)
            y = diametro / 2 * math.sin(angulo)
            puntos.append((x, y, z))

    return puntos

# Ejemplo de uso
diametro = 50  # Diámetro del cilindro en milímetros
altura = 100   # Altura del cilindro en milímetros
pasos = 50     # Cantidad de puntos por círculo
niveles = 10   # Cantidad de círculos a lo largo del eje Z
puntos_cilindro = generar_puntos_para_cilindro_perpendicular(diametro, altura, pasos, niveles)

# Extraer las coordenadas x, y, y z de los puntos
x_coords, y_coords, z_coords = zip(*puntos_cilindro)

# Graficar los puntos en 3D
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(x_coords, y_coords, z_coords, marker='o')

ax.set_xlabel('X (mm)')
ax.set_ylabel('Y (mm)')
ax.set_zlabel('Z (mm)')
ax.set_title('Código G para un cilindro perpendicular')

plt.show()
