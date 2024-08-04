import os
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import re

# Variables globales para almacenar la última ubicación y el último nombre personalizado
ultima_ubicacion = os.getcwd()
ultimo_nombre_personalizado = ""

def get_next_numbered_name(nombre_base, numero_inicial):
    # Buscar un número al final del nombre base del archivo
    match = re.search(r"_(\d+)$", nombre_base)
    if match:
        numero = int(match.group(1))
        return re.sub(r"_(\d+)$", f"_{numero + 1}", nombre_base)
    else:
        return f"{nombre_base}_{numero_inicial}"

def rename_files(archivos_seleccionados, nombre_personalizado, numero_inicial):
    try:
        for archivo_seleccionado in archivos_seleccionados:
            directorio = os.path.dirname(archivo_seleccionado)
            nombre_base, extension = os.path.splitext(os.path.basename(archivo_seleccionado))

            nombre_nuevo = f"{nombre_personalizado}_{numero_inicial}"

            # Renombrar el archivo seleccionado y los siguientes archivos con el mismo nombre base
            while os.path.exists(os.path.join(directorio, f"{nombre_nuevo}{extension}")):
                numero_inicial += 1
                nombre_nuevo = f"{nombre_personalizado}_{numero_inicial}"

            nombre_nuevo = os.path.join(directorio, f"{nombre_nuevo}{extension}")
            os.rename(archivo_seleccionado, nombre_nuevo)
            numero_inicial += 1
        
        messagebox.showinfo("Éxito", "Se ha cambiado el nombre de los archivos correctamente!",
                            icon=messagebox.INFO, parent=ventana)
    except Exception as e:
        messagebox.showerror("Error", "Algo ha fallado, intenta de nuevo: " + str(e),
                             icon=messagebox.ERROR, parent=ventana)

def examinar_archivos():
    global ultima_ubicacion, ultimo_nombre_personalizado  # Acceder a las variables globales
    ventana.withdraw()  # Ocultar la ventana principal mientras se muestra el cuadro de diálogo de examinar
    archivos_seleccionados = filedialog.askopenfilenames(filetypes=[("Archivos de Imagen", "*.jpg;*.jpeg;*.png;*.gif"),
                                                                    ("Todos los archivos", "*.*")],
                                                        initialdir=ultima_ubicacion,
                                                        multiple=True)
    ventana.deiconify()  # Mostrar nuevamente la ventana principal
    if archivos_seleccionados:
        ultima_ubicacion = os.path.dirname(archivos_seleccionados[0])  # Actualizar la última ubicación
        # Cuadro de diálogo para obtener el nombre personalizado
        nombre_personalizado = simpledialog.askstring("Nombre Personalizado", "Ingresa el nombre que desees:",
                                                      initialvalue=ultimo_nombre_personalizado)
        if nombre_personalizado:
            ultimo_nombre_personalizado = nombre_personalizado  # Guardar el último nombre personalizado
            numero_inicial = simpledialog.askinteger("Número Inicial", "Ingresa el número inicial:",
                                                     initialvalue=1)
            if numero_inicial is not None:
                rename_files(archivos_seleccionados, nombre_personalizado, numero_inicial)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("ArchiveRewritter")

# Permitir mover la ventana principal
def mover_ventana(event):
    ventana.geometry('+{0}+{1}'.format(event.x_root, event.y_root))

barra_superior = tk.Frame(ventana, bg='cyan')
barra_superior.pack(fill='x', expand=1)
barra_superior.bind('<B1-Motion>', mover_ventana)

# Botón de examinar
boton_examinar = tk.Button(ventana, text="Examinar", command=examinar_archivos)
boton_examinar.pack(pady=20)

ventana.mainloop()
