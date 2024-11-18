import time

import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
pi = math.pi

# Función para generar el código G para una esfera
def generate_g_code_for_sphere(radius=120, step=10, file_out='sphere_gcode.gcode', speed=450):
    with open(file_out, 'w') as archivo:
        # Escribir configuraciones iniciales
        # archivo.write("G21\n")  # Establecer unidades en milímetros
        # archivo.write("G17\n")  # Seleccionar plano XY
        # archivo.write("G90\n")  # Posicionamiento absoluto

        g_code = []
        # Iniciar en el punto más alto de la esfera
        # g_code.append((0, 0, radius))

        # Generar el código G para cada capa de la esfera
        for z in range(-radius, radius + 1, step):
            # Calcular el radio de la sección circular a esa altura
            current_radius = round(math.sqrt(radius ** 2 - z ** 2),2)

            # Calcular el ángulo de paso, asegurando que no sea cero
            step_angle = (step / (0.1 + current_radius)) * (180 / pi)
            step_angle = max(1, int(step_angle))  # Asegurar que el paso mínimo sea 1

            # Generar los puntos de corte en la circunferencia
            for theta in range(0, 360, step_angle):
                x = round(current_radius * math.cos(math.radians(theta)), 2)
                y = round(current_radius * math.sin(math.radians(theta)), 2)
                g_code.append((x, y, z, speed))

                # Escribir comando G-code para mover al siguiente punto
                archivo.write(f"G21 G17 G90 G1 X{x:.2f} Y{y:.2f} Z{z:.2f} F{speed}\n")

        archivo.write("M30\n")  # Fin del programa
        # print(g_code)
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

def calcular_tiempo_de_recorrido(nombre_archivo):
    tiempo_total = 0
    ultima_x = ultima_y = ultima_z = None
    with open(nombre_archivo, 'r') as archivo:
        for linea in archivo:
            if linea.startswith("G1"):
                valores = linea.split()
                velocidad = None
                distancia = None
                for valor in valores:
                    if valor.startswith("F"):
                        velocidad = float(valor[1:])
                    elif valor.startswith("X"):
                        x = float(valor[1:])
                    elif valor.startswith("Y"):
                        y = float(valor[1:])
                    elif valor.startswith("Z"):
                        z = float(valor[1:])
                if ultima_x is not None and ultima_y is not None and ultima_z is not None:
                    distancia = ((x - ultima_x) ** 2 + (y - ultima_y) ** 2 + (z - ultima_z) ** 2) ** 0.5
                if velocidad and distancia:
                    tiempo = distancia / velocidad
                    tiempo_total += tiempo
                ultima_x = x
                ultima_y = y
                ultima_z = z
    return tiempo_total

# Parámetros de la esfera
# radius = 65
# step = 1
#
# # Llamar a la función para graficar la esfera con la simulación del código G
# plot_sphere_with_g_code(radius, step)
generate_g_code_for_sphere()
tiempo_recorrido = calcular_tiempo_de_recorrido("sphere_gcode.gcode")
print("Tiempo de recorrido total:", tiempo_recorrido, "minutos")