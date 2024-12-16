import tkinter as tk
import pyodbc
from funciones.show import visual
from funciones.agregar import agregardatos
from funciones.modificar import modificaciones
from funciones.delete import borrar_dato
from cerrar.close import cerrar_conexion

# Configuración de la base de datos
SERVER = 'Leandro'  
DATABASE = 'Drinkers'
connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;'

try:
    # Intenta conectar
    conn = pyodbc.connect(connectionString)
    print("Conexión exitosa")
except pyodbc.Error as e:
    print(f"Error al conectar o ejecutar la consulta: {e}")

# Crear la ventana principal
root = tk.Tk()  
root.title("Drinkers")
root.geometry("400x600")
root["bg"]="#D4AF37"
root.iconbitmap("logo.ico")

# Crear un marco para el menú
menu_marco = tk.Frame(root)
menu_marco.pack(pady=10)
menu_marco["bg"]="#D4AF37"

# Crear título
titulo = tk.Label(menu_marco, text="Bienvenidos a Drinkers", font=("Arial", 20, "bold"))
titulo.pack(pady=10)

# Botón para abrir funciones
def mostrar_entradas():
     
    # Limpiar el marco anterior (si existe)
    for widget in menu_marco.winfo_children():
        widget.destroy()
   

    # Crear un marco nuevo para las entradas
    entrada_frame = tk.Frame(root)
    entrada_frame.pack(pady=10)
    entrada_frame["bg"]="#D4AF37"
    
    boton_show = tk.Button(entrada_frame, text="Visualizar registros", font=("Arial", 12), command= lambda: visual(root, conn))
    boton_show.pack(pady=10)

    boton_add = tk.Button(entrada_frame, text="Agregar registros", font=("Arial", 12), command= lambda: agregardatos(root, conn))
    boton_add.pack(pady=10)

    boton_change = tk.Button(entrada_frame, text="Modificar registros", font=("Arial", 12), command= lambda: modificaciones(root, conn))
    boton_change.pack(pady=10)

    boton_delete = tk.Button(entrada_frame, text="Eliminar registros", font=("Arial", 12), command=lambda: borrar_dato(root, conn))
    boton_delete.pack(pady=10)

    boton_sa = tk.Button(entrada_frame, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexion(root, conn))
    boton_sa.pack(pady=10)

    # Mostrar los elementos en la ventana
    entrada_frame.pack(pady=10)

# Botón para ingresar datos
boton_input = tk.Button(menu_marco, text="Funciones", font=("Arial", 12), command=mostrar_entradas)
boton_input.pack(pady=10)

# Botón para salir
boton_salir = tk.Button(menu_marco, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexion(root, conn))
boton_salir.pack(pady=10)


root.mainloop()
