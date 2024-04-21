import math

def generar_codigo_g_para_cilindro_vertical(diametro, altura, pasos=100, velocidad=100):
    codigo_g = []

    # Definir la altura del cilindro
    codigo_g.append(f"G0 Z0")  # Mover a la altura inicial
    codigo_g.append(f"G1 F{velocidad} Z{altura}")  # Bajar hasta la altura del cilindro

    # Generar el contorno del cilindro
    for i in range(pasos + 1):
        angulo = i * (2 * math.pi / pasos)
        x = diametro / 2 * math.cos(angulo)
        y = diametro / 2 * math.sin(angulo)
        codigo_g.append(f"G1 X{x:.2f} Y{y:.2f}")  # Mover a la posición siguiente

    # Volver al punto inicial
    codigo_g.append(f"G1 X{diametro/2:.2f} Y0")

    # Subir a la altura inicial
    codigo_g.append(f"G0 Z{altura}")

    return codigo_g

def exportar_codigo_g_a_archivo(codigo_g, nombre_archivo):
    with open(nombre_archivo, 'w') as archivo:
        for linea in codigo_g:
            archivo.write(linea + '\n')

# Ejemplo de uso
diametro = 50  # Diámetro del cilindro en milímetros
altura = 100   # Altura del cilindro en milímetros
codigo_g_cilindro = generar_codigo_g_para_cilindro_vertical(diametro, altura)

# Nombre del archivo de salida
nombre_archivo = 'codigo_g_cilindro.txt'

# Exportar el código G generado a un archivo de texto
exportar_codigo_g_a_archivo(codigo_g_cilindro, nombre_archivo)
