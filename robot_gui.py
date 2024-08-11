import tkinter as tk
from tkinter import scrolledtext

def conectar():
    output_terminal.insert(tk.END, "Conectado\n")

def desconectar():
    output_terminal.insert(tk.END, "Desconectado\n")

def simular():
    output_terminal.insert(tk.END, "Simulación en progreso...\n")

def iniciar():
    output_terminal.insert(tk.END, "Iniciando...\n")

def parar():
    output_terminal.insert(tk.END, "Parado\n")

def mover_arriba():
    output_terminal.insert(tk.END, "Moviendo hacia arriba\n")

def mover_abajo():
    output_terminal.insert(tk.END, "Moviendo hacia abajo\n")

def mover_izquierda():
    output_terminal.insert(tk.END, "Moviendo hacia la izquierda\n")

def mover_derecha():
    output_terminal.insert(tk.END, "Moviendo hacia la derecha\n")

def definir_origen_x():
    output_terminal.insert(tk.END, "Origen X definido\n")

def definir_origen_y():
    output_terminal.insert(tk.END, "Origen Y definido\n")

def definir_origen_z():
    output_terminal.insert(tk.END, "Origen Z definido\n")

def definir_origen():
    output_terminal.insert(tk.END, "Origen general definido\n")

root = tk.Tk()
root.title("Simulador")

# Sección de conexión
frame_conexion = tk.Frame(root, bd=2, relief="solid")
frame_conexion.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

tk.Label(frame_conexion, text="Selector de puerto").grid(row=0, column=0, padx=5, pady=5)
tk.Button(frame_conexion, text="Conectar", command=conectar).grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame_conexion, text="Desconectar", command=desconectar).grid(row=0, column=2, padx=5, pady=5)

# Sección de controles y parámetros
frame_parametros = tk.Frame(root, bd=2, relief="solid")
frame_parametros.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

tk.Label(frame_parametros, text="Campo para definir R").grid(row=0, column=0, padx=5, pady=5)
tk.Label(frame_parametros, text="Campo para definir tiempo").grid(row=1, column=0, padx=5, pady=5)
tk.Label(frame_parametros, text="Para definir puntos").grid(row=2, column=0, padx=5, pady=5)

tk.Entry(frame_parametros).grid(row=0, column=1, padx=5, pady=5)
tk.Entry(frame_parametros).grid(row=1, column=1, padx=5, pady=5)
tk.Entry(frame_parametros).grid(row=2, column=1, padx=5, pady=5)

tk.Button(frame_parametros, text="Simular", command=simular).grid(row=3, column=0, padx=5, pady=5)
tk.Button(frame_parametros, text="Iniciar", command=iniciar).grid(row=3, column=1, padx=5, pady=5)

# Sección de movimiento
frame_movimiento = tk.Frame(root, bd=2, relief="solid")
frame_movimiento.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

tk.Button(frame_movimiento, text="Arriba", command=mover_arriba).grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame_movimiento, text="Izquierda", command=mover_izquierda).grid(row=1, column=0, padx=5, pady=5)
tk.Button(frame_movimiento, text="Centro", command=lambda: None).grid(row=1, column=1, padx=5, pady=5)
tk.Button(frame_movimiento, text="Derecha", command=mover_derecha).grid(row=1, column=2, padx=5, pady=5)
tk.Button(frame_movimiento, text="Abajo", command=mover_abajo).grid(row=2, column=1, padx=5, pady=5)

# Sección de origen
frame_origen = tk.Frame(root, bd=2, relief="solid")
frame_origen.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")

tk.Button(frame_origen, text="Origen X", command=definir_origen_x).grid(row=0, column=0, padx=5, pady=5)
tk.Button(frame_origen, text="Origen Y", command=definir_origen_y).grid(row=1, column=0, padx=5, pady=5)
tk.Button(frame_origen, text="Origen Z", command=definir_origen_z).grid(row=2, column=0, padx=5, pady=5)
tk.Button(frame_origen, text="Origen", command=definir_origen).grid(row=3, column=0, padx=5, pady=5)

# Sección de gráficas de lectura
frame_graficas = tk.Frame(root, bd=2, relief="solid")
frame_graficas.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")
tk.Label(frame_graficas, text="Gráficos de lectura").pack(padx=5, pady=5)

# Sección de tabla
frame_tabla = tk.Frame(root, bd=2, relief="solid")
frame_tabla.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

for i in range(5):
    tk.Label(frame_tabla, text=f"Columna {i+1}").grid(row=0, column=i, padx=5, pady=5)

# Sección de terminal de salida
frame_terminal = tk.Frame(root, bd=2, relief="solid")
frame_terminal.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

output_terminal = scrolledtext.ScrolledText(frame_terminal, wrap=tk.WORD, height=10)
output_terminal.pack(fill=tk.BOTH, expand=True)

# Botón de parar
tk.Button(root, text="PARAR", command=parar, fg="red").grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

root.mainloop()
