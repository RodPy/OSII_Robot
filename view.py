import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
class RobotCNCApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Robot CNC Control")
        self.geometry("800x600")

        # Parte 1: Conexiones Seriales
        # Variables para los puertos seriales seleccionados
        self.selected_port_A = tk.StringVar()
        self.selected_port_B = tk.StringVar()

        # Parte 1: Conexiones Seriales
        serial_frame = ttk.Frame(self)
        serial_frame.pack(fill=tk.X)

        # Dispositivo A
        serial_label_A = ttk.Label(serial_frame, text="Puerto Serial Dispositivo A:")
        serial_label_A.grid(row=0, column=0)

        self.serial_ports_A = self.get_serial_ports()
        self.serial_combobox_A = ttk.Combobox(serial_frame, values=self.serial_ports_A,
                                              textvariable=self.selected_port_A)
        self.serial_combobox_A.grid(row=0, column=1)

        # Dispositivo B
        serial_label_B = ttk.Label(serial_frame, text="Puerto Serial Dispositivo B:")
        serial_label_B.grid(row=1, column=0)

        self.serial_ports_B = self.get_serial_ports()
        self.serial_combobox_B = ttk.Combobox(serial_frame, values=self.serial_ports_B,
                                              textvariable=self.selected_port_B)
        self.serial_combobox_B.grid(row=1, column=1)

        connect_button = ttk.Button(serial_frame, text="Conectar", command=self.connect)
        connect_button.grid(row=0, column=2, rowspan=2)

        # Parte 2: Configuración de Movimiento
        config_frame = ttk.Frame(self)
        config_frame.pack(fill=tk.BOTH, expand=True)

        # Columna 1
        entry_frame = ttk.LabelFrame(config_frame, text="Configuración de Movimiento")
        entry_frame.grid(row=0, column=0, padx=10, pady=10)

        length_label = ttk.Label(entry_frame, text="Longitud (mm):")
        length_label.grid(row=0, column=0, sticky=tk.W)
        length_entry = ttk.Entry(entry_frame)
        length_entry.grid(row=0, column=1)
        length_entry.insert(0, "100")

        speed_label = ttk.Label(entry_frame, text="Velocidad (mm/min):")
        speed_label.grid(row=1, column=0, sticky=tk.W)
        speed_entry = ttk.Entry(entry_frame)
        speed_entry.grid(row=1, column=1)
        speed_entry.insert(0, "50")

        steps_label = ttk.Label(entry_frame, text="Pasos (mm):")
        steps_label.grid(row=2, column=0, sticky=tk.W)
        steps_entry = ttk.Entry(entry_frame)
        steps_entry.grid(row=2, column=1)
        steps_entry.insert(0, "10")

        # Columna 2
        config_frame = ttk.Frame(self)
        config_frame.pack(fill=tk.BOTH, expand=True)

        # Gráfico
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=config_frame)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # Añadir los radio buttons
        self.sensor_var = tk.StringVar()
        sensor_frame = ttk.Frame(config_frame)
        sensor_frame.pack(side=tk.LEFT, padx=10)

        ttk.Radiobutton(sensor_frame, text="X Sensor", variable=self.sensor_var, value="X_SENSOR", command=self.update_graph).pack(anchor=tk.W)
        ttk.Radiobutton(sensor_frame, text="Y Sensor", variable=self.sensor_var, value="Y_SENSOR", command=self.update_graph).pack(anchor=tk.W)
        ttk.Radiobutton(sensor_frame, text="Z Sensor", variable=self.sensor_var, value="Z_SENSOR", command=self.update_graph).pack(anchor=tk.W)

        # Actualizar el gráfico según la selección inicial
        self.update_graph()

        # Imagen
        self.image_frame = ttk.Frame(config_frame)
        self.image_frame.pack(side=tk.LEFT, padx=10)

        # Cargar la imagen por defecto
        self.load_image("img/img1.jpg")

        # Parte 3: Tabla de Proceso
        table_frame = ttk.Frame(self)
        table_frame.pack(fill=tk.BOTH, expand=True)

        treeview = ttk.Treeview(table_frame, columns=("X_code", "Y_code", "Z_code", "X_sensor", "Y_sensor", "Z_sensor"))
        treeview.heading("#0", text="ID")
        treeview.heading("X_code", text="X Code")
        treeview.heading("Y_code", text="Y Code")
        treeview.heading("Z_code", text="Z Code")
        treeview.heading("X_sensor", text="X Sensor")
        treeview.heading("Y_sensor", text="Y Sensor")
        treeview.heading("Z_sensor", text="Z Sensor")
        treeview.pack(fill=tk.BOTH, expand=True)

        # Botón Descornectar
        disconnect_button = ttk.Button(self, text="Desconectar", command=self.disconnect)
        disconnect_button.pack(side=tk.BOTTOM)


    def update_graph(self):
        # Lógica para actualizar el gráfico según la selección del radio button
        sensor = self.sensor_var.get()
        x = [1, 2, 3, 4, 5]
        y = [5, 4, 3, 2, 1]
        self.ax.clear()
        self.ax.plot(x, y)
        self.ax.set_xlabel("Tiempo")
        self.ax.set_ylabel(sensor)
        self.canvas.draw()

        # Cargar la imagen según el radio button seleccionado
        if sensor == "X_SENSOR":
            self.load_image("img/img1.jpg")
        elif sensor == "Y_SENSOR":
            self.load_image("img/img2.jpg")
        elif sensor == "Z_SENSOR":
            self.load_image("img/img3.jpg")

    def load_image(self, filename):
        # Limpiar cualquier imagen previamente cargada
        for widget in self.image_frame.winfo_children():
            widget.destroy()

        # Cargar y mostrar la nueva imagen
        image = Image.open(filename)
        image = image.resize((50, 50))
        photo = ImageTk.PhotoImage(image)
        image_label = ttk.Label(self.image_frame, image=photo)
        image_label.image = photo
        image_label.pack()

        # Parte 3: Tabla de Proceso
        table_frame = ttk.Frame(self)
        table_frame.pack(fill=tk.BOTH, expand=True)

        treeview = ttk.Treeview(table_frame, columns=("X_code", "Y_code", "Z_code", "X_sensor", "Y_sensor", "Z_sensor"))
        treeview.heading("#0", text="ID")
        treeview.heading("X_code", text="X Code")
        treeview.heading("Y_code", text="Y Code")
        treeview.heading("Z_code", text="Z Code")
        treeview.heading("X_sensor", text="X Sensor")
        treeview.heading("Y_sensor", text="Y Sensor")
        treeview.heading("Z_sensor", text="Z Sensor")
        treeview.pack(fill=tk.BOTH, expand=True)

        # Botón Descornectar
        disconnect_button = ttk.Button(self, text="Desconectar", command=self.disconnect)
        disconnect_button.pack(side=tk.BOTTOM)

    def get_serial_ports(self):
        ports = [port.device for port in serial.tools.list_ports.comports()]
        return ports

    def connect(self):
        port_A = self.selected_port_A.get()
        port_B = self.selected_port_B.get()

        try:
            # Conexión al puerto serial para Dispositivo A
            serial_connection_A = serial.Serial(port_A, baudrate=9600, timeout=1)
            print(f"Conectado al puerto serial para Dispositivo A: {port_A}")
        except serial.SerialException as e:
            print(f"Error al conectar al puerto serial para Dispositivo A: {e}")

        try:
            # Conexión al puerto serial para Dispositivo B
            serial_connection_B = serial.Serial(port_B, baudrate=9600, timeout=1)
            print(f"Conectado al puerto serial para Dispositivo B: {port_B}")
        except serial.SerialException as e:
            print(f"Error al conectar al puerto serial para Dispositivo B: {e}")

        # Aquí puedes almacenar las conexiones serial en variables de instancia si necesitas usarlas posteriormente

    def get_serial_ports(self):
        ports = [port.device for port in serial.tools.list_ports.comports()]
        return ports

    def connect(self):
        selected_port = self.serial_combobox.get()
        # Aquí puedes implementar la lógica de conexión al puerto serial seleccionado
        print(f"Conectado al puerto serial: {selected_port}")

    def update_graph(self):
        # Lógica para actualizar el gráfico según la selección del radio button
        sensor = self.sensor_var.get()
        x = [1, 2, 3, 4, 5]
        y = [5, 4, 3, 2, 1]
        self.ax.clear()
        self.ax.plot(x, y)
        self.ax.set_xlabel("Tiempo")
        self.ax.set_ylabel(sensor)
        self.canvas.draw()

    def disconnect(self):
        # Aquí puedes implementar la lógica de desconexión serial
        print("Desconectado")

if __name__ == "__main__":
    app = RobotCNCApp()
    app.mainloop()
