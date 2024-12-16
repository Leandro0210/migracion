import tkinter as tk
import psycopg2
from cerrarpo.closepostg import *
from funcionpostgre.funcionespostgre import *
from clase.conexion import *

def interfaz():

 db_manager = DatabaseManager(database="Drinkers", user="postgres", host="localhost", password="HalaMadrid",  port="5432")
 conn_postgres = db_manager.connect()

    # Crear la ventana principal
 ruut = tk.Tk()
 ruut.title("Drinkers")
 ruut.geometry("400x600")
 ruut["bg"]="#D4AF37"
 ruut.iconbitmap("logo.ico")

 # Crear un marco para el menú
 menu_marco = tk.Frame(ruut)
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
    entrada_frame = tk.Frame(ruut)
    entrada_frame.pack(pady=10)
    entrada_frame["bg"]="#D4AF37"
    # Botón para llamar la función visual()
    boton_show = tk.Button(entrada_frame, text="Visualizar registros", font=("Arial", 12), command=lambda: mostrarpostgre(ruut, conn_postgres))
    boton_show.pack(pady=10)

    # Botón para llamar la función
    boton_add = tk.Button(entrada_frame, text="Agregar registros", font=("Arial", 12), command= lambda: agregarpostgre(ruut, conn_postgres))
    boton_add.pack(pady=10)

    # Botón para llamar la función
    boton_change = tk.Button(entrada_frame, text="Modificar registros", font=("Arial", 12), command= lambda: modificarpostgre(ruut, conn_postgres))
    boton_change.pack(pady=10)

    # Botón para llamar la función
    boton_delete = tk.Button(entrada_frame, text="Eliminar registros", font=("Arial", 12), command= lambda: borrardatos_postgre(ruut, conn_postgres))
    boton_delete.pack(pady=10)

    # Botón para llamar la función
    boton_sa = tk.Button(entrada_frame, text="Salir", font=("Arial", 12),  command=lambda: cerrar_conexionpostgre(ruut, conn_postgres))
    boton_sa.pack(pady=10)

    # Mostrar los elementos en la ventana
    entrada_frame.pack(pady=10)
 
 # Botón para ingresar datos
 boton_input = tk.Button(menu_marco, text="Funciones", font=("Arial", 12), command=mostrar_entradas)
 boton_input.pack(pady=10)

 # Botón para salir
 boton_salir = tk.Button(menu_marco, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexionpostgre(ruut, conn_postgres))
 boton_salir.pack(pady=10)


 ruut.mainloop()

 

