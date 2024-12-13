import tkinter as tk
from tablas.empleado import agre_emp
from tablas.cliente import agre_cli
from tablas.producto import agre_pro
from tablas.ventas import agre_ven
from tablas.detalle import agre_de
from cerrar.close import cerrar_conexion

def agrego(root, conn):  
    # Limpiar la ventana principal
    for widget in root.winfo_children():
        widget.destroy()

    # Crear un nuevo marco dentro de root
    op = tk.Frame(root)
    op.pack(pady=10)
    op["bg"]="#D4AF37"

    cli_boton = tk.Button(op, text="Clientes", font=("Arial", 12), command=lambda: agre_cli(root, conn))  #
    cli_boton.pack(pady=10)

    de_boton = tk.Button(op, text="Detalles Venta", font=("Arial", 12), command=lambda: agre_de(root, conn)) #
    de_boton.pack(pady=10)

    pro_boton = tk.Button(op, text="Productos", font=("Arial", 12), command=lambda: agre_pro(root, conn)) #
    pro_boton.pack(pady=10)


    ve_boton = tk.Button(op, text="Ventas", font=("Arial", 12), command=lambda: agre_ven(root, conn)) #
    ve_boton.pack(pady=10)

    emp_boton = tk.Button(op, text="Empleados", font=("Arial", 12), command=lambda: agre_emp(root, conn)) 
    emp_boton.pack(pady=10)

    # Botón para salir
    volver_boton = tk.Button(op, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexion(root, conn))
    volver_boton.pack(pady=10)