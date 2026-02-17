"""
robot_gui.py
Interfaz gráfica simulador: conexión serial, simulación, controles de movimiento y origen.
Simulator GUI: serial connection, simulation, movement and origin controls.
Author: Rodney Rojas
Sustainable MRI Lab
February 2026
Version: 1.0
"""
import sys
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox
import serial
import serial.tools.list_ports
import main
import visual_bd_test

class SimuladorApp:
    """Interfaz de simulación y control del robot OSII."""

    STEP_MM = 10  # Paso de movimiento en mm
    FEED_RATE = 400

    def __init__(self, root):
        self.root = root
        self.root.title("OSII Robot - Simulador")
        self.root.minsize(700, 550)
        self.root.geometry("800x600")
        self.serial = None  # Conexión CNC
        self.gaussmeter = None  # Conexión Gaussmeter
        self._running_thread = None
        self._stop_flag = threading.Event()

        self._setup_styles()
        self._create_variables()
        self._create_ui()
        self._configure_grid()
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _setup_styles(self):
        """Configura estilos ttk."""
        style = ttk.Style()
        style.configure("TFrame", padding=5)
        style.configure("Header.TLabel", font=("", 10, "bold"))

    def _create_variables(self):
        """Crea variables de control."""
        self.port_cnc_var = tk.StringVar()
        self.port_gaussmeter_var = tk.StringVar()
        self.baud_var = tk.StringVar(value="115200")
        self.radius_var = tk.StringVar(value="110")
        self.sample_time_var = tk.StringVar(value="7")
        self.step_var = tk.StringVar(value="10")

    def _create_ui(self):
        """Construye la interfaz."""
        # --- Sección conexión ---
        conn_frame = ttk.LabelFrame(self.root, text="Conexión Serial", padding=8)
        conn_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        # Fila CNC
        ttk.Label(conn_frame, text="CNC:").grid(row=0, column=0, padx=(0, 5), pady=2, sticky="w")
        self.port_cnc_combo = ttk.Combobox(conn_frame, textvariable=self.port_cnc_var, width=18, state="readonly")
        self.port_cnc_combo.grid(row=0, column=1, padx=5, pady=2)
        ttk.Label(conn_frame, text="Baud:").grid(row=0, column=2, padx=(5, 2), pady=2)
        ttk.Entry(conn_frame, textvariable=self.baud_var, width=8).grid(row=0, column=3, padx=2, pady=2)
        self.btn_connect_cnc = ttk.Button(conn_frame, text="Conectar CNC", command=self._conectar_cnc)
        self.btn_connect_cnc.grid(row=0, column=4, padx=5)
        self.btn_disconnect_cnc = ttk.Button(conn_frame, text="Desconectar", command=self._desconectar_cnc, state=tk.DISABLED)
        self.btn_disconnect_cnc.grid(row=0, column=5, padx=2)

        # Fila Gaussmeter
        ttk.Label(conn_frame, text="Gaussmeter:").grid(row=1, column=0, padx=(0, 5), pady=2, sticky="w")
        self.port_gaussmeter_combo = ttk.Combobox(conn_frame, textvariable=self.port_gaussmeter_var, width=18, state="readonly")
        self.port_gaussmeter_combo.grid(row=1, column=1, padx=5, pady=2)
        self.btn_connect_gaussmeter = ttk.Button(conn_frame, text="Conectar Gaussmeter", command=self._conectar_gaussmeter)
        self.btn_connect_gaussmeter.grid(row=1, column=4, padx=5)
        self.btn_disconnect_gaussmeter = ttk.Button(conn_frame, text="Desconectar", command=self._desconectar_gaussmeter, state=tk.DISABLED)
        self.btn_disconnect_gaussmeter.grid(row=1, column=5, padx=2)

        ttk.Button(conn_frame, text="Actualizar puertos", command=self._refresh_ports).grid(row=0, column=6, rowspan=2, padx=15)
        self._refresh_ports()

        # --- Parámetros de escaneo ---
        param_frame = ttk.LabelFrame(self.root, text="Parámetros de Escaneo", padding=8)
        param_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        ttk.Label(param_frame, text="Radio (mm):").grid(row=0, column=0, padx=5, pady=3, sticky="w")
        ttk.Entry(param_frame, textvariable=self.radius_var, width=10).grid(row=0, column=1, padx=5, pady=3)

        ttk.Label(param_frame, text="Tiempo muestra (s):").grid(row=1, column=0, padx=5, pady=3, sticky="w")
        ttk.Entry(param_frame, textvariable=self.sample_time_var, width=10).grid(row=1, column=1, padx=5, pady=3)

        ttk.Label(param_frame, text="Paso (mm):").grid(row=2, column=0, padx=5, pady=3, sticky="w")
        ttk.Entry(param_frame, textvariable=self.step_var, width=10).grid(row=2, column=1, padx=5, pady=3)

        ttk.Separator(param_frame, orient="horizontal").grid(row=3, column=0, columnspan=2, sticky="ew", pady=8)

        self.btn_simular = ttk.Button(param_frame, text="Simular (visualización)", command=self._simular)
        self.btn_simular.grid(row=4, column=0, columnspan=2, pady=5)
        self.btn_iniciar = ttk.Button(param_frame, text="Iniciar escaneo completo", command=self._iniciar)
        self.btn_iniciar.grid(row=5, column=0, columnspan=2, pady=5)

        # --- Controles de movimiento ---
        move_frame = ttk.LabelFrame(self.root, text="Movimiento (Jog)", padding=8)
        move_frame.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")

        ttk.Button(move_frame, text="▲\nArriba", command=lambda: self._mover(0, 1, 0)).grid(row=0, column=1, padx=3, pady=3)
        ttk.Button(move_frame, text="◀ Izq", command=lambda: self._mover(-1, 0, 0)).grid(row=1, column=0, padx=3, pady=3)
        ttk.Button(move_frame, text="Centro", command=self._ir_centro).grid(row=1, column=1, padx=3, pady=3)
        ttk.Button(move_frame, text="Der ▶", command=lambda: self._mover(1, 0, 0)).grid(row=1, column=2, padx=3, pady=3)
        ttk.Button(move_frame, text="▼\nAbajo", command=lambda: self._mover(0, -1, 0)).grid(row=2, column=1, padx=3, pady=3)

        # --- Origen ---
        orig_frame = ttk.LabelFrame(self.root, text="Definir Origen", padding=8)
        orig_frame.grid(row=1, column=2, padx=10, pady=5, sticky="nsew")

        ttk.Button(orig_frame, text="Origen X", command=lambda: self._enviar_gcode("G28 X")).pack(fill=tk.X, pady=3)
        ttk.Button(orig_frame, text="Origen Y", command=lambda: self._enviar_gcode("G28 Y")).pack(fill=tk.X, pady=3)
        ttk.Button(orig_frame, text="Origen Z", command=lambda: self._enviar_gcode("G28 Z")).pack(fill=tk.X, pady=3)
        ttk.Button(orig_frame, text="Origen (G28)", command=lambda: self._enviar_gcode("G28")).pack(fill=tk.X, pady=3)
        ttk.Button(orig_frame, text="Unlock ($X)", command=lambda: self._enviar_gcode("$X")).pack(fill=tk.X, pady=3)

        ttk.Separator(orig_frame, orient="horizontal").pack(fill=tk.X, pady=5)
        ttk.Button(orig_frame, text="Leer Gaussmeter", command=self._leer_gaussmeter).pack(fill=tk.X, pady=3)

        # --- Terminal ---
        term_frame = ttk.LabelFrame(self.root, text="Terminal", padding=5)
        term_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

        self.terminal = scrolledtext.ScrolledText(term_frame, wrap=tk.WORD, height=10, state=tk.DISABLED)
        self.terminal.pack(fill=tk.BOTH, expand=True)

        # --- Botón parar ---
        self.btn_parar = ttk.Button(self.root, text="⏹ PARAR", command=self._parar)
        self.btn_parar.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

    def _configure_grid(self):
        """Configura pesos de filas/columnas para redimensionado."""
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(2, weight=1)

    def _get_available_ports(self):
        """Obtiene lista de puertos seriales disponibles."""
        ports = [p.device for p in serial.tools.list_ports.comports()]
        if sys.platform == "win32":
            for p in ("COM3", "COM4"):
                if p not in ports:
                    ports.append(p)
        else:
            for p in ("/dev/ttyACM0", "/dev/ttyUSB0"):
                if p not in ports:
                    ports.append(p)
        return sorted(ports)

    def _refresh_ports(self):
        """Actualiza la lista de puertos en ambos selectores."""
        ports = self._get_available_ports()
        self.port_cnc_combo["values"] = ports
        self.port_gaussmeter_combo["values"] = ports
        if ports:
            if not self.port_cnc_var.get():
                self.port_cnc_var.set("/dev/ttyACM0" if "/dev/ttyACM0" in ports else ports[0])
            if not self.port_gaussmeter_var.get():
                default_g = "/dev/ttyUSB0" if sys.platform != "win32" else "COM4"
                self.port_gaussmeter_var.set(default_g if default_g in ports else ports[-1] if len(ports) > 1 else ports[0])

    def _log(self, msg, level="info"):
        """Escribe mensaje en terminal."""
        self.terminal.configure(state=tk.NORMAL)
        prefix = {"info": "", "ok": "[OK] ", "err": "[Error] "}.get(level, "")
        self.terminal.insert(tk.END, f"{prefix}{msg}\n")
        self.terminal.see(tk.END)
        self.terminal.configure(state=tk.DISABLED)
        self.root.update_idletasks()

    def _conectar_cnc(self):
        """Establece conexión serial con el CNC."""
        puerto = self.port_cnc_var.get().strip()
        if not puerto:
            messagebox.showwarning("Aviso", "Seleccione un puerto para el CNC.")
            return
        try:
            baud = int(self.baud_var.get())
        except ValueError:
            messagebox.showerror("Error", "Velocidad de baudios inválida.")
            return
        try:
            self.serial = serial.Serial(port=puerto, baudrate=baud, timeout=1)
            self.btn_connect_cnc.configure(state=tk.DISABLED)
            self.btn_disconnect_cnc.configure(state=tk.NORMAL)
            self._log(f"CNC conectado: {puerto} @ {baud} bps", "ok")
        except serial.SerialException as e:
            self._log(str(e), "err")
            messagebox.showerror("Error de conexión CNC", str(e))

    def _desconectar_cnc(self):
        """Cierra conexión serial del CNC."""
        if self.serial and self.serial.is_open:
            self.serial.close()
            self.serial = None
        self.btn_connect_cnc.configure(state=tk.NORMAL)
        self.btn_disconnect_cnc.configure(state=tk.DISABLED)
        self._log("CNC desconectado.")

    def _conectar_gaussmeter(self):
        """Establece conexión con el Gaussmeter."""
        puerto = self.port_gaussmeter_var.get().strip()
        if not puerto:
            messagebox.showwarning("Aviso", "Seleccione un puerto para el Gaussmeter.")
            return
        if not GaussmeterReader:
            self._log("GaussmeterReader no disponible.", "err")
            return
        try:
            self.gaussmeter = GaussmeterReader(magnetometer_port=puerto)
            self.btn_connect_gaussmeter.configure(state=tk.DISABLED)
            self.btn_disconnect_gaussmeter.configure(state=tk.NORMAL)
            self._log(f"Gaussmeter conectado: {puerto}", "ok")
        except Exception as e:
            self._log(str(e), "err")
            messagebox.showerror("Error de conexión Gaussmeter", str(e))

    def _desconectar_gaussmeter(self):
        """Cierra conexión del Gaussmeter."""
        if self.gaussmeter:
            try:
                self.gaussmeter.close()
            except Exception:
                pass
            self.gaussmeter = None
        self.btn_connect_gaussmeter.configure(state=tk.NORMAL)
        self.btn_disconnect_gaussmeter.configure(state=tk.DISABLED)
        self._log("Gaussmeter desconectado.")

    def _leer_gaussmeter(self):
        """Lee y muestra valor del gaussmeter en el terminal."""
        if not self.gaussmeter:
            self._log("Conecte primero el Gaussmeter.", "err")
            return
        try:
            valor = self.gaussmeter.read_gaussmeter()
            self._log(f"Gaussmeter: {valor:.4f} Gauss", "ok")
        except Exception as e:
            self._log(str(e), "err")

    def _enviar_gcode(self, gcode):
        """Envía código G al CNC si hay conexión."""
        if not self.serial or not self.serial.is_open:
            self._log("Conectar primero el puerto serial.", "err")
            return
        cmd = f"{gcode.strip()}\n"
        try:
            self.serial.write(cmd.encode("utf-8"))
            self._log(f"Enviado: {gcode.strip()}")
        except serial.SerialException as e:
            self._log(str(e), "err")

    def _mover(self, dx, dy, dz):
        """Movimiento relativo (incremental)."""
        step = self.STEP_MM
        x = dx * step
        y = dy * step
        z = dz * step
        cmd = f"G91 G1 X{x:.1f} Y{y:.1f} Z{z:.1f} F{self.FEED_RATE}"
        self._enviar_gcode(cmd)
        dirs = []
        if dx: dirs.append("derecha" if dx > 0 else "izquierda")
        if dy: dirs.append("arriba" if dy > 0 else "abajo")
        if dz: dirs.append("Z+" if dz > 0 else "Z-")
        if dirs:
            self._log(f"Movimiento: {', '.join(dirs)}")

    def _ir_centro(self):
        """Va al centro (0,0,0)."""
        self._enviar_gcode("G90 G1 X0 Y0 Z0 F400")
        self._log("Moviendo a centro (0,0,0)")

    def _simular(self):
        """Abre visualización 3D en tiempo real (en thread)."""
        if not MODULES_AVAILABLE:
            self._log("Módulos main/visual_bd_test no disponibles.", "err")
            return
        self._log("Iniciando visualización 3D...")
        def run():
            try:
                visual_bd_test.plot()
            except Exception as e:
                self.root.after(0, lambda: self._log(str(e), "err"))
        threading.Thread(target=run, daemon=True).start()

    def _iniciar(self):
        """Inicia escaneo completo (main) en thread."""
        if not MODULES_AVAILABLE:
            self._log("Módulo main no disponible.", "err")
            return
        if self._running_thread and self._running_thread.is_alive():
            self._log("Escaneo ya en ejecución.", "err")
            return
        self._log("Iniciando escaneo completo (main)...")
        def run():
            try:
                main.main()
                self.root.after(0, lambda: self._log("Escaneo finalizado.", "ok"))
            except Exception as e:
                self.root.after(0, lambda: self._log(str(e), "err"))
        self._running_thread = threading.Thread(target=run, daemon=True)
        self._running_thread.start()

    def _parar(self):
        """Indica parada (el thread actual no se detiene; útil para feedback)."""
        self._stop_flag.set()
        self._log("Solicitud de parada enviada.")
        # Nota: main.main() no comprueba esta bandera; se necesita modificar main para soporte real.

    def _on_closing(self):
        """Cierra ventana de forma segura."""
        self._desconectar_cnc()
        self._desconectar_gaussmeter()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorApp(root)
    root.mainloop()
