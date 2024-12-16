import tkinter as tk
from tablas.empleado import agregar_empleado
from tablas.cliente import agregar_cliente
from tablas.producto import agregar_producto
from tablas.ventas import agregar_venta
from tablas.detalle import agregar_detalle
from cerrar.close import cerrar_conexion

def agregardatos(root, conn):  
    # Limpiar la ventana principal
    for widget in root.winfo_children():
        widget.destroy()

    # Crear un nuevo marco dentro de root
    new_marco = tk.Frame(root)
    new_marco.pack(pady=10)
    new_marco["bg"]="#D4AF37"

    cliente_boton = tk.Button(new_marco, text="Clientes", font=("Arial", 12), command=lambda: agregar_cliente(root, conn))  #
    cliente_boton.pack(pady=10)

    detalle_boton = tk.Button(new_marco, text="Detalles Venta", font=("Arial", 12), command=lambda: agregar_detalle(root, conn)) #
    detalle_boton.pack(pady=10)

    producto_boton = tk.Button(new_marco, text="Productos", font=("Arial", 12), command=lambda: agregar_producto(root, conn)) #
    producto_boton.pack(pady=10)


    venta_boton = tk.Button(new_marco, text="Ventas", font=("Arial", 12), command=lambda: agregar_venta(root, conn)) #
    venta_boton.pack(pady=10)

    empleado_boton = tk.Button(new_marco, text="Empleados", font=("Arial", 12), command=lambda: agregar_empleado(root, conn)) 
    empleado_boton.pack(pady=10)

    volver_boton = tk.Button(new_marco, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexion(root, conn))
    volver_boton.pack(pady=10)