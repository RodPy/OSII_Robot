import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import serial
import time

# Configuración de la conexión serial
ser = serial.Serial('COM3', 115200, timeout=1)

# Función para enviar código G desde la entrada de texto
def send_gcode():
    gcode = gcode_entry.get("1.0", tk.END)
    if gcode.strip():
        ser.write(gcode.encode('utf-8'))
        time.sleep(1)  # Esperar un momento para obtener la respuesta
        response = ser.read(ser.in_waiting).decode('utf-8')
        response_text.insert(tk.END, response + "\n")
    else:
        messagebox.showwarning("Advertencia", "La entrada de código G está vacía.")

# Función para cargar y enviar un archivo G-code
def load_gcode_file():
    file_path = filedialog.askopenfilename(filetypes=[("G-code files", "*.gcode"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'r') as file:
            for line in file:
                ser.write(line.encode('utf-8'))
                time.sleep(0.1)  # Pausa entre líneas para no saturar el buffer serial
                response = ser.read(ser.in_waiting).decode('utf-8')
                if response:
                    response_text.insert(tk.END, response + "\n")
        messagebox.showinfo("Información", "Archivo G-code enviado exitosamente.")

# Crear la ventana principal
root = tk.Tk()
root.title("Envío de código G")

# Crear un marco para la entrada de código G
frame = tk.Frame(root)
frame.pack(pady=10)

# Etiqueta y entrada de texto para el código G
tk.Label(frame, text="Ingrese el código G:").pack(anchor='w')
gcode_entry = scrolledtext.ScrolledText(frame, width=50, height=10)
gcode_entry.pack(padx=5, pady=5)

# Botón para enviar el código G
send_button = tk.Button(frame, text="Enviar código G", command=send_gcode)
send_button.pack(pady=5)

# Botón para cargar un archivo G-code
load_button = tk.Button(frame, text="Cargar archivo G-code", command=load_gcode_file)
load_button.pack(pady=5)

# Área de texto para mostrar la respuesta del dispositivo
tk.Label(root, text="Respuesta del dispositivo:").pack(anchor='w')
response_text = scrolledtext.ScrolledText(root, width=60, height=15)
response_text.pack(padx=5, pady=5)

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()

# Cerrar la conexión serial al salir
ser.close()
