import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import serial.tools.list_ports
import main
import visual_bd_test

class SimuladorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador")
        self.serial = None  # Inicializa el atributo de conexión serial

        # Variables
        self.port_var = tk.StringVar()
        self.baud_var = tk.StringVar(value="9600")

        # Sección de conexión
        self.frame_conexion = tk.Frame(self.root, bd=2, relief="solid")
        self.frame_conexion.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        tk.Label(self.frame_conexion, text="Selector de puerto").grid(row=0, column=0, padx=5, pady=5)
        self.port_combobox = ttk.Combobox(self.frame_conexion, textvariable=self.port_var, values=self.listar_puertos())
        self.port_combobox.grid(row=0, column=1, padx=10, pady=10)

        self.connect_button = tk.Button(self.frame_conexion, text="Conectar", command=self.conectar)
        self.connect_button.grid(row=0, column=2, padx=5, pady=5)

        self.disconnect_button = tk.Button(self.frame_conexion, text="Desconectar", command=self.desconectar,
                                           state=tk.DISABLED)
        self.disconnect_button.grid(row=0, column=3, padx=5, pady=5)

        # Sección de controles y parámetros
        self.frame_parametros = tk.Frame(self.root, bd=2, relief="solid")
        self.frame_parametros.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        tk.Label(self.frame_parametros, text="Campo para definir R").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(self.frame_parametros).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.frame_parametros, text="Campo para definir tiempo").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(self.frame_parametros).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.frame_parametros, text="Para definir puntos").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(self.frame_parametros).grid(row=2, column=1, padx=5, pady=5)

        tk.Button(self.frame_parametros, text="Simular", command=self.simular).grid(row=3, column=0, padx=5, pady=5)
        tk.Button(self.frame_parametros, text="Iniciar", command=self.iniciar).grid(row=3, column=1, padx=5, pady=5)

        # Sección de movimiento
        self.frame_movimiento = tk.Frame(self.root, bd=2, relief="solid")
        self.frame_movimiento.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        tk.Button(self.frame_movimiento, text="Arriba", command=self.mover_arriba).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.frame_movimiento, text="Izquierda", command=self.mover_izquierda).grid(row=1, column=0, padx=5,
                                                                                              pady=5)
        tk.Button(self.frame_movimiento, text="Centro", command=lambda: None).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self.frame_movimiento, text="Derecha", command=self.mover_derecha).grid(row=1, column=2, padx=5,
                                                                                          pady=5)
        tk.Button(self.frame_movimiento, text="Abajo", command=self.mover_abajo).grid(row=2, column=1, padx=5, pady=5)

        # Sección de origen
        self.frame_origen = tk.Frame(self.root, bd=2, relief="solid")
        self.frame_origen.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

        tk.Button(self.frame_origen, text="Origen X", command=self.definir_origen_x).grid(row=0, column=0, padx=5,
                                                                                          pady=5)
        tk.Button(self.frame_origen, text="Origen Y", command=self.definir_origen_y).grid(row=1, column=0, padx=5,
                                                                                          pady=5)
        tk.Button(self.frame_origen, text="Origen Z", command=self.definir_origen_z).grid(row=2, column=0, padx=5,
                                                                                          pady=5)
        tk.Button(self.frame_origen, text="Origen", command=self.definir_origen).grid(row=3, column=0, padx=5, pady=5)

        # Sección de gráficas de lectura
        self.frame_graficas = tk.Frame(self.root, bd=2, relief="solid")
        self.frame_graficas.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")
        tk.Label(self.frame_graficas, text="Gráficos de lectura").pack(padx=5, pady=5)

        # Sección de tabla
        self.frame_tabla = tk.Frame(self.root, bd=2, relief="solid")
        self.frame_tabla.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        for i in range(5):
            tk.Label(self.frame_tabla, text=f"Columna {i + 1}").grid(row=0, column=i, padx=5, pady=5)

        # Sección de terminal de salida
        self.frame_terminal = tk.Frame(self.root, bd=2, relief="solid")
        self.frame_terminal.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        self.output_terminal = scrolledtext.ScrolledText(self.frame_terminal, wrap=tk.WORD, height=10)
        self.output_terminal.pack(fill=tk.BOTH, expand=True)

        # Botón de parar
        tk.Button(self.root, text="PARAR", command=self.parar, fg="red").grid(row=4, column=0, columnspan=3, padx=10,
                                                                              pady=10, sticky="ew")

    def listar_puertos(self):
        # Obtener una lista de puertos seriales disponibles
        puertos_disponibles = [port.device for port in serial.tools.list_ports.comports()]
        # Agregar COM5 como opción
        if 'COM5' not in puertos_disponibles:
            puertos_disponibles.append('COM5')
        return puertos_disponibles

    def conectar(self):
        self.output_terminal.insert(tk.END, "Conectado\n")

        # Conectar al puerto serial seleccionado con la velocidad especificada
        puerto = self.port_var.get()
        velocidad = int(self.baud_var.get())

        try:
            self.serial = serial.Serial(port=puerto, baudrate=velocidad, timeout=1)
            self.connect_button.configure(state=tk.DISABLED)
            self.disconnect_button.configure(state=tk.NORMAL)
            print(f"Conectado a {puerto} a {velocidad} bps")
        except serial.SerialException as e:
            print(f"Error al conectar: {e}")

    def desconectar(self):
        self.output_terminal.insert(tk.END, "Desconectado\n")

        # Desconectar el puerto serial
        if self.serial:
            self.serial.close()
            self.connect_button.configure(state=tk.NORMAL)
            self.disconnect_button.configure(state=tk.DISABLED)
            print("Desconectado")

    def simular(self):
        self.output_terminal.insert(tk.END, "Simulación en progreso...\n")
        visual_bd_test.plot()

    def iniciar(self):
        self.output_terminal.insert(tk.END, "Iniciando...\n")
        main.main()

    def parar(self):
        self.output_terminal.insert(tk.END, "Parado\n")

    def mover_arriba(self):
        self.output_terminal.insert(tk.END, "Moviendo hacia arriba\n")

    def mover_abajo(self):
        self.output_terminal.insert(tk.END, "Moviendo hacia abajo\n")

    def mover_izquierda(self):
        self.output_terminal.insert(tk.END, "Moviendo hacia la izquierda\n")

    def mover_derecha(self):
        self.output_terminal.insert(tk.END, "Moviendo hacia la derecha\n")

    def definir_origen_x(self):
        self.output_terminal.insert(tk.END, "Origen X definido\n")

    def definir_origen_y(self):
        self.output_terminal.insert(tk.END, "Origen Y definido\n")

    def definir_origen_z(self):
        self.output_terminal.insert(tk.END, "Origen Z definido\n")

    def definir_origen(self):
        self.output_terminal.insert(tk.END, "Origen general definido\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorApp(root)
    root.mainloop()
