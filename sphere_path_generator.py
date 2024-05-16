import time

import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Función para generar el código G para una esfera
def generate_g_code_for_sphere(radius, step):
    g_code = []

    # Iniciar en el punto más alto de la esfera
    g_code.append((0, 0, radius))

    # Generar el código G para cada capa de la esfera
    for y in range(-radius, radius + 1, step):
        # Calcular el radio de la sección circular a esa altura
        current_radius = round(math.sqrt(radius ** 2 - y ** 2),2)

        # Generar los puntos de corte en la circunferencia
        for theta in range(0, 360, 5):
            x = round(current_radius * math.cos(math.radians(theta)),2)
            z = round(current_radius * math.sin(math.radians(theta)),2)
            g_code.append((x, y, z))

    return g_code

# Función para graficar una esfera con sus puntos y simulación del código G
def plot_sphere_with_g_code(radius, step):
    # Generar el código G para la esfera
    g_code = generate_g_code_for_sphere(radius, step)

    # Crear la figura y el objeto de los ejes 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Graficar la esfera
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = radius * np.outer(np.cos(u), np.sin(v))
    y = radius * np.outer(np.sin(u), np.sin(v))
    z = radius * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x, y, z, color='b', alpha=0.5)

    # Graficar puntos de corte generados por el código G
    for i in range(len(g_code) - 1):
        ax.plot([g_code[i][0], g_code[i + 1][0]],
                [g_code[i][1], g_code[i + 1][1]],
                [g_code[i][2], g_code[i + 1][2]], color='y')

    # Configuración de los ejes
    ax.set_xlim([-radius, radius])
    ax.set_ylim([-radius, radius])
    ax.set_zlim([-radius, radius])

    # Etiquetas de los ejes
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Mostrar la gráfica
    plt.show()

# Parámetros de la esfera
radius = 20
step = 1

# Llamar a la función para graficar la esfera con la simulación del código G
plot_sphere_with_g_code(radius, step)
