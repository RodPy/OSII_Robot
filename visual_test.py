import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Función para actualizar la imagen
def update_image():
    selection = selected_option.get()
    if selection == 1:
        img = Image.open("image1.jpg")  # Cambia "image1.png" por tu imagen
    elif selection == 2:
        img = Image.open("image2.jpg")  # Cambia "image2.png" por tu imagen
    elif selection == 3:
        img = Image.open("image3.jpg")  # Cambia "image3.png" por tu imagen

    img = img.resize((100, 100), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(img)
    image_label.config(image=photo)
    image_label.image = photo

# Configuración de la ventana principal
root = tk.Tk()
root.title("Selector de imágenes")

# Variable para la opción seleccionada
selected_option = tk.IntVar()

# Crear y colocar los botones de radio
radio1 = ttk.Radiobutton(root, text="Opción 1", variable=selected_option, value=1, command=update_image)
radio2 = ttk.Radiobutton(root, text="Opción 2", variable=selected_option, value=2, command=update_image)
radio3 = ttk.Radiobutton(root, text="Opción 3", variable=selected_option, value=3, command=update_image)

radio1.pack()
radio2.pack()
radio3.pack()

# Crear y colocar el label para mostrar la imagen
image_label = ttk.Label(root)
image_label.pack()

# Establecer la opción predeterminada
selected_option.set(1)
update_image()

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()
