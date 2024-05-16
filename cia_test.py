import tkinter as tk
from tkinter import ttk
import serial
import math

class InterfazImpresora3D:
    def __init__(self, root):
        self.root = root
        self.root.title("Control de Trayectoria")

        # Variables para almacenar los valores del radio, velocidad y pasos
        self.radio_var = tk.DoubleVar()
        self.velocidad_var = tk.DoubleVar()
        self.pasos_var = tk.IntVar()

        # Crear etiquetas y campos de entrada para el radio, velocidad y pasos
        self.label_radio = ttk.Label(root, text="Radio:")
        self.entry_radio = ttk.Entry(root, textvariable=self.radio_var)

        self.label_velocidad = ttk.Label(root, text="Velocidad:")
        self.entry_velocidad = ttk.Entry(root, textvariable=self.velocidad_var)

        self.label_pasos = ttk.Label(root, text="Pasos:")
        self.entry_pasos = ttk.Entry(root, textvariable=self.pasos_var)

        # Crear botones para enviar comandos G-code y generar trayectoria
        self.btn_enviar_gcode = ttk.Button(root, text="Enviar G-code", command=self.enviar_gcode)
        self.btn_generar_trayectoria = ttk.Button(root, text="Generar Trayectoria", command=self.enviar_gcode_trayectoria)
        self.btn_origen_x = ttk.Button(root, text="Origen X", command=lambda: self.enviar_gcode("G28 X"))
        self.btn_origen_y = ttk.Button(root, text="Origen Y", command=lambda: self.enviar_gcode("G28 Y"))
        self.btn_origen_z = ttk.Button(root, text="Origen Z", command=lambda: self.enviar_gcode("G28 Z"))
        self.btn_desconectar_serial = ttk.Button(root, text="Desconectar Serial", command=self.desconectar_serial)

        # Posicionar los elementos en la interfaz
        self.label_radio.grid(row=0, column=0, padx=10, pady=5)
        self.entry_radio.grid(row=0, column=1, padx=10, pady=5)
        self.label_velocidad.grid(row=1, column=0, padx=10, pady=5)
        self.entry_velocidad.grid(row=1, column=1, padx=10, pady=5)
        self.label_pasos.grid(row=2, column=0, padx=10, pady=5)
        self.entry_pasos.grid(row=2, column=1, padx=10, pady=5)
        self.btn_enviar_gcode.grid(row=3, column=0, columnspan=2, pady=10)
        self.btn_generar_trayectoria.grid(row=4, column=0, columnspan=2, pady=10)
        self.btn_origen_x.grid(row=5, column=0, pady=5)
        self.btn_origen_y.grid(row=5, column=1, pady=5)
        self.btn_origen_z.grid(row=6, column=0, pady=5)
        self.btn_desconectar_serial.grid(row=6, column=1, pady=5)

        # Configurar conexión serial
        self.serial_port = serial.Serial('COM7', 115200)  # Ajusta el puerto y la velocidad según tu configuración

    def generar_trayectoria(self):
        radio = self.radio_var.get()
        pasos = self.pasos_var.get()
        trayectoria = []

        for i in range(pasos):
            theta = 2 * math.pi * i / pasos
            x = radio * math.cos(theta)
            y = radio * math.sin(theta)
            z = 0  # Puedes ajustar la altura en la esfera según tus necesidades
            trayectoria.append((x, y, z))

        return trayectoria

    def enviar_gcode(self, gcode=None):
        if gcode is None:
            radio = self.radio_var.get()
            velocidad = self.velocidad_var.get()
            gcode = f"G2 R{radio} F{velocidad}"  # Ejemplo de comando G-code para trayectoria circular
        self.serial_port.write((gcode + '\n').encode('utf-8'))

    def enviar_gcode_trayectoria(self):
        trayectoria = self.generar_trayectoria()

        for punto in trayectoria:
            gcode = f"G1 X{punto[0]} Y{punto[1]} Z{punto[2]} F{self.velocidad_var.get()}"
            self.serial_port.write((gcode + '\n').encode('utf-8'))

    def desconectar_serial(self):
        self.serial_port.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazImpresora3D(root)
    root.mainloop()
