import tkinter as tk
from tablas.cliente import borrar_cliente
from tablas.detalle import borrar_detalle
from tablas.producto import borrar_producto
from tablas.ventas import borrar_venta
from tablas.empleado import borrar_empleado
from cerrar.close import cerrar_conexion

def borrar_dato(root, conn):  
    # Limpiar la ventana principal
    for widget in root.winfo_children():
        widget.destroy()

    # Crear un nuevo marco dentro de root
    new_marco = tk.Frame(root)
    new_marco.pack(pady=10)
    new_marco["bg"] = "#D4AF37"
   
    cliente_boton = tk.Button(new_marco, text="Clientes", font=("Arial", 12), command=lambda: borrar_cliente(root, conn))  
    cliente_boton.pack(pady=10)

    detalle_boton = tk.Button(new_marco, text="Detalles Venta", font=("Arial", 12), command=lambda: borrar_detalle(root, conn)) 
    detalle_boton.pack(pady=10)

    producto_boton = tk.Button(new_marco, text="Productos", font=("Arial", 12), command=lambda: borrar_producto(root, conn)) 
    producto_boton.pack(pady=10)

    venta_boton = tk.Button(new_marco, text="Ventas", font=("Arial", 12), command=lambda: borrar_venta(root, conn)) 
    venta_boton.pack(pady=10)

    empleado_boton = tk.Button(new_marco, text="Empleados", font=("Arial", 12), command=lambda: borrar_empleado(root, conn)) 
    empleado_boton.pack(pady=10)

    volver_boton = tk.Button(new_marco, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexion(root, conn))
    volver_boton.pack(pady=10)