import tkinter as tk
from tablas.categoria import mues_cate
from tablas.cliente import mues_cli
from tablas.detalle import mues_de
from tablas.producto import mues_pro
from tablas.subcategoria import mues_sub
from tablas.ventas import mues_ven
from tablas.empleado import mues_emp
from cerrar.close import cerrar_conexion
def visual(root, conn):  
    # Limpiar la ventana principal
    for widget in root.winfo_children():
        widget.destroy()

    # Crear un nuevo marco dentro de root
    op = tk.Frame(root)
    op.pack(pady=10)
    op["bg"]="#D4AF37"
    # Creo botones con comandos
    c_boton = tk.Button(op, text="Categorías", font=("Arial", 12), command=lambda: mues_cate(conn))
    c_boton.pack(pady=10)

    cli_boton = tk.Button(op, text="Clientes", font=("Arial", 12), command=lambda: mues_cli(conn))
    cli_boton.pack(pady=10)

    de_boton = tk.Button(op, text="Detalles Venta", font=("Arial", 12), command=lambda: mues_de(conn))
    de_boton.pack(pady=10)

    pro_boton = tk.Button(op, text="Productos", font=("Arial", 12), command=lambda: mues_pro(conn))
    pro_boton.pack(pady=10)

    sub_boton = tk.Button(op, text="Subcategorías", font=("Arial", 12), command=lambda: mues_sub(conn))
    sub_boton.pack(pady=10)

    ve_boton = tk.Button(op, text="Ventas", font=("Arial", 12), command=lambda: mues_ven(conn))
    ve_boton.pack(pady=10)

    emp_boton = tk.Button(op, text="Empleados", font=("Arial", 12), command=lambda: mues_emp(conn))
    emp_boton.pack(pady=10)

    # Botón para volver al menú principal
    volver_boton = tk.Button(op, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexion(root, conn))
    volver_boton.pack(pady=10)