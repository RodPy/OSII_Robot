import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports

class Impresora3DApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Control de Impresora 3D")

        self.port_label = ttk.Label(root, text="Puerto Serial:")
        self.port_label.grid(row=0, column=0, padx=10, pady=10)

        self.port_var = tk.StringVar()
        self.port_combobox = ttk.Combobox(root, textvariable=self.port_var, values=self.listar_puertos())
        self.port_combobox.grid(row=0, column=1, padx=10, pady=10)

        self.actualizar_button = ttk.Button(root, text="Actualizar Puertos", command=self.actualizar_puertos)
        self.actualizar_button.grid(row=0, column=2, padx=10, pady=10)

        self.baud_label = ttk.Label(root, text="Velocidad (bps):")
        self.baud_label.grid(row=1, column=0, padx=10, pady=10)

        self.baud_var = tk.StringVar()
        self.baud_combobox = ttk.Combobox(root, textvariable=self.baud_var, values=["9600", "115200"])
        self.baud_combobox.grid(row=1, column=1, padx=10, pady=10)

        self.connect_button = ttk.Button(root, text="Conectar", command=self.conectar)
        self.connect_button.grid(row=2, column=0, padx=10, pady=10)

        self.disconnect_button = ttk.Button(root, text="Desconectar", command=self.desconectar, state=tk.DISABLED)
        self.disconnect_button.grid(row=2, column=1, padx=10, pady=10)

        self.codigo_g_label = ttk.Label(root, text="Código G:")
        self.codigo_g_label.grid(row=3, column=0, padx=10, pady=10)

        self.codigo_g_entry = ttk.Entry(root, width=30)
        self.codigo_g_entry.grid(row=3, column=1, padx=10, pady=10)

        self.enviar_button = ttk.Button(root, text="Enviar Código G", command=self.enviar_codigo_g, state=tk.DISABLED)
        self.enviar_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.serial = None

    def listar_puertos(self):
        # Obtener una lista de puertos seriales disponibles
        puertos_disponibles = [port.device for port in serial.tools.list_ports.comports()]
        # Agregar COM5 como opción
        if 'COM5' not in puertos_disponibles:
            puertos_disponibles.append('COM5')
        return puertos_disponibles

    def actualizar_puertos(self):
        # Actualizar la lista de puertos seriales
        self.port_combobox['values'] = self.listar_puertos()

    def conectar(self):
        # Conectar al puerto serial seleccionado con la velocidad especificada
        puerto = self.port_var.get()
        velocidad = int(self.baud_var.get())

        try:
            self.serial = serial.Serial(port=puerto, baudrate=velocidad, timeout=1)
            self.connect_button.configure(state=tk.DISABLED)
            self.disconnect_button.configure(state=tk.NORMAL)
            self.enviar_button.configure(state=tk.NORMAL)
            print(f"Conectado a {puerto} a {velocidad} bps")
        except serial.SerialException as e:
            print(f"Error al conectar: {e}")

    def desconectar(self):
        # Desconectar el puerto serial
        if self.serial:
            self.serial.close()
            self.connect_button.configure(state=tk.NORMAL)
            self.disconnect_button.configure(state=tk.DISABLED)
            self.enviar_button.configure(state=tk.DISABLED)
            print("Desconectado")

    def enviar_codigo_g(self):
        # Enviar el código G por el puerto serial
        codigo_g = self.codigo_g_entry.get()
        codigo_g =f'{codigo_g}\n'
        if self.serial and self.serial.is_open:
            try:
                self.serial.write(codigo_g.encode('utf-8'))
                print(f"Código G enviado: {codigo_g}\n")
            except Exception as e:
                print(f"Error al enviar código G: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Impresora3DApp(root)
    root.mainloop()
