import tkinter as tk
from tablas.categoria import mostrar_categoria
from tablas.cliente import mostrar_clientes
from tablas.detalle import mostrar_detalles
from tablas.producto import mostrar_productos
from tablas.subcategoria import mostrar_subcateg
from tablas.ventas import mostrar_ventas
from tablas.empleado import mostrar_empleados
from cerrar.close import cerrar_conexion
def visual(root, conn):  
    # Limpiar la ventana principal
    for widget in root.winfo_children():
        widget.destroy()

    # Crear un nuevo marco dentro de root
    new_marco = tk.Frame(root)
    new_marco.pack(pady=10)
    new_marco["bg"]="#D4AF37"
    # Creo botones con comandos
    categoria_boton = tk.Button(new_marco, text="Categorías", font=("Arial", 12), command=lambda: mostrar_categoria(conn))
    categoria_boton.pack(pady=10)

    cliente_boton = tk.Button(new_marco, text="Clientes", font=("Arial", 12), command=lambda: mostrar_clientes(conn))
    cliente_boton.pack(pady=10)

    borrar_boton = tk.Button(new_marco, text="Detalles Venta", font=("Arial", 12), command=lambda: mostrar_detalles(conn))
    borrar_boton.pack(pady=10)

    producto_boton = tk.Button(new_marco, text="Productos", font=("Arial", 12), command=lambda: mostrar_productos(conn))
    producto_boton.pack(pady=10)

    subcateg_boton = tk.Button(new_marco, text="Subcategorías", font=("Arial", 12), command=lambda: mostrar_subcateg(conn))
    subcateg_boton.pack(pady=10)

    venta_boton = tk.Button(new_marco, text="Ventas", font=("Arial", 12), command=lambda: mostrar_ventas(conn))
    venta_boton.pack(pady=10)

    empleado_boton = tk.Button(new_marco, text="Empleados", font=("Arial", 12), command=lambda: mostrar_empleados(conn))
    empleado_boton.pack(pady=10)

    # Botón para volver al menú principal
    volver_boton = tk.Button(new_marco, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexion(root, conn))
    volver_boton.pack(pady=10)