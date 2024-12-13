import tkinter as tk
from tablas.empleado import mod_emp
from tablas.producto import mod_pro
from tablas.cliente import mod_cli
from cerrar.close import cerrar_conexion

def cambios(root, conn):  
    # Limpiar la ventana principal
    for widget in root.winfo_children():
        widget.destroy()

    # Crear un nuevo marco dentro de root
    op = tk.Frame(root)
    op.pack(pady=10)
    op["bg"] = "#D4AF37"
   
    cli_boton = tk.Button(op, text="Clientes", font=("Arial", 12), command=lambda: mod_cli(root, conn))  
    cli_boton.pack(pady=10)

    pro_boton = tk.Button(op, text="Productos", font=("Arial", 12), command=lambda: mod_pro(root, conn)) #
    pro_boton.pack(pady=10)

    emp_boton = tk.Button(op, text="Empleados", font=("Arial", 12), command=lambda: mod_emp(root, conn)) 
    emp_boton.pack(pady=10)

    volver_boton = tk.Button(op, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexion(root, conn))
    volver_boton.pack(pady=10)