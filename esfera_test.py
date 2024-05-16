import math

def generar_esfera(archivo_salida, velocidad_avance, cantidad_puntos, radio):
    with open(archivo_salida, 'w') as archivo:
        # Escribir configuraciones iniciales
        archivo.write("G21\n")  # Establecer unidades en milímetros
        archivo.write("G17\n")  # Seleccionar plano XY
        archivo.write("G90\n")  # Posicionamiento absoluto

        # Calcular ángulo entre puntos
        angulo_entre_puntos = 360 / cantidad_puntos

        # Definir el radio de la esfera (convertir a mm)
        radio_mm = radio * 10

        # Iniciar trazado de la esfera
        for i in range(cantidad_puntos):
            theta = math.radians(i * angulo_entre_puntos)
            x = radio_mm * math.cos(theta)
            y = radio_mm * math.sin(theta)
            z = 0  # Por ahora, asumimos que la esfera está en el plano XY

            # Escribir comando G-code para mover al siguiente punto
            archivo.write(f"G1 X{x:.2f} Y{y:.2f} Z{z:.2f} F{velocidad_avance}\n")

        # Escribir comando de finalización
        archivo.write("M30\n")  # Fin del programa

# Ejemplo de uso
archivo_salida = "esfera.gcode"
velocidad_avance = 100  # mm/min
cantidad_puntos = 100  # Cantidad de puntos para aproximar la esfera
radio = 1  # Radio de la esfera en cm

generar_esfera(archivo_salida, velocidad_avance, cantidad_puntos, radio)
print(f"Archivo {archivo_salida} generado con éxito.")
