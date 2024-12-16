import tkinter as tk
from tablas.empleado import modificar_empleado
from tablas.producto import modificar_producto
from tablas.cliente import modificar_cliente
from cerrar.close import cerrar_conexion

def modificaciones(root, conn):  
    # Limpiar la ventana principal
    for widget in root.winfo_children():
        widget.destroy()

    # Crear un nuevo marco dentro de root
    new_marco = tk.Frame(root)
    new_marco.pack(pady=10)
    new_marco["bg"] = "#D4AF37"
   
    cliente_boton = tk.Button(new_marco, text="Clientes", font=("Arial", 12), command=lambda: modificar_cliente(root, conn))  
    cliente_boton.pack(pady=10)

    producto_boton = tk.Button(new_marco, text="Productos", font=("Arial", 12), command=lambda: modificar_producto(root, conn)) #
    producto_boton.pack(pady=10)

    empleado_boton = tk.Button(new_marco, text="Empleados", font=("Arial", 12), command=lambda: modificar_empleado(root, conn)) 
    empleado_boton.pack(pady=10)

    volver_boton = tk.Button(new_marco, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexion(root, conn))
    volver_boton.pack(pady=10)