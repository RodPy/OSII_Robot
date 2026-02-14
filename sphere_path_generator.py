"""
October 2024 - Version 3.0 (optimized)
Author: Rodney Rojas - Sustainable MRI Lab

sphere_path_generator.py
Genera G-code para una trayectoria esférica 3D (CNC/additive). Incluye opción de
visualización y guardado en archivo.
"""
import math
from typing import List, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 - needed for projection='3d'

# Constantes precalculadas
DEG_PER_RAD = 180.0 / math.pi


def generate_g_code_for_sphere(
    radius: int = 120,
    step: int = 10,
    file_out: Optional[str] = "sphere_gcode.gcode",
    speed: int = 450,
) -> List[Tuple[float, float, float, int]]:
    """
    Genera lista de puntos (x, y, z, speed) para una esfera y opcionalmente escribe G-code.

    :param radius: Radio en mm.
    :param step: Paso en altura (mm) entre capas.
    :param file_out: Ruta del archivo G-code; None para no escribir.
    :param speed: Avance en mm/min.
    :return: Lista de (x, y, z, speed).
    """
    g_code: List[Tuple[float, float, float, int]] = []
    z_values = range(-radius, radius + 1, step)

    for z in z_values:
        r_sq = radius ** 2 - z ** 2
        if r_sq < 0:
            continue
        current_radius = round(math.sqrt(r_sq), 2)
        if current_radius <= 0:
            g_code.append((0.0, 0.0, float(z), speed))
            continue

        step_angle = max(1, int((step / (0.1 + current_radius)) * DEG_PER_RAD))
        thetas = range(0, 360, step_angle)
        for theta in thetas:
            rad = math.radians(theta)
            x = round(current_radius * math.cos(rad), 2)
            y = round(current_radius * math.sin(rad), 2)
            g_code.append((x, y, float(z), speed))

    if file_out:
        _write_gcode_file(file_out, g_code, speed)
    return g_code


def _write_gcode_file(
    path: str,
    points: List[Tuple[float, float, float, int]],
    speed: int,
) -> None:
    """Escribe los puntos en un archivo G-code."""
    with open(path, "w") as f:
        for x, y, z, sp in points:
            f.write(f"G1 X{x:.2f} Y{y:.2f} Z{z:.2f} F{sp}\n")
        f.write("M30\n")


def plot_sphere_with_g_code(radius: int, step: int) -> None:
    """Dibuja la esfera y la trayectoria generada por el G-code."""
    g_code = generate_g_code_for_sphere(radius, step, file_out=None)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x_s = radius * np.outer(np.cos(u), np.sin(v))
    y_s = radius * np.outer(np.sin(u), np.sin(v))
    z_s = radius * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x_s, y_s, z_s, color="b", alpha=0.5)

    pts = np.array(g_code)
    if len(pts) >= 2:
        ax.plot(pts[:, 0], pts[:, 1], pts[:, 2], color="y", linewidth=0.5)

    ax.set_xlim([-radius, radius])
    ax.set_ylim([-radius, radius])
    ax.set_zlim([-radius, radius])
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.show()
