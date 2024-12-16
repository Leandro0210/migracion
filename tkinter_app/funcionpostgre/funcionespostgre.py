import tkinter as tk
from tablaspostgre.categoriapostg import categoria_postgres
from tablaspostgre.clientepostg import *
from tablaspostgre.detallepostg import *
from tablaspostgre.productospostg import *
from tablaspostgre.subcategoriapostg import *
from tablaspostgre.ventaspostg import *
from tablaspostgre.empleadopostg import *
from cerrarpo.closepostg import cerrar_conexionpostgre

def mostrarpostgre(ruut, conn_postgres):  
    # Limpiar la ventana principal
    for widget in ruut.winfo_children():
        widget.destroy()

    # Crear un nuevo marco dentro de root
    new_marco = tk.Frame(ruut)
    new_marco.pack(pady=10)
    new_marco["bg"]="#D4AF37"
    
    categoria_boton = tk.Button(new_marco, text="Categorías", font=("Arial", 12), command= lambda: categoria_postgres(ruut, conn_postgres))
    categoria_boton.pack(pady=10)

    cliente_boton = tk.Button(new_marco, text="Clientes", font=("Arial", 12), command= lambda: cliente_postgre(ruut, conn_postgres))
    cliente_boton.pack(pady=10)

    detalle_boton = tk.Button(new_marco, text="Detalles Venta", font=("Arial", 12), command= lambda: detalle_postgre(ruut, conn_postgres))
    detalle_boton.pack(pady=10)

    producto_boton = tk.Button(new_marco, text="Productos", font=("Arial", 12), command= lambda: producto_postgre(ruut, conn_postgres))
    producto_boton.pack(pady=10)

    subcateg_boton = tk.Button(new_marco, text="Subcategorías", font=("Arial", 12), command= lambda: subcategoria_postgre(ruut, conn_postgres))
    subcateg_boton.pack(pady=10)

    venta_boton = tk.Button(new_marco, text="Ventas", font=("Arial", 12), command= lambda: ventas_postgre(ruut, conn_postgres))
    venta_boton.pack(pady=10)

    empleado_boton = tk.Button(new_marco, text="Empleados", font=("Arial", 12), command= lambda: empleado_postgre(ruut, conn_postgres))
    empleado_boton.pack(pady=10)

    # Botón para salir
    volver_boton = tk.Button(new_marco, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexionpostgre(ruut, conn_postgres))
    volver_boton.pack(pady=10)


def agregarpostgre(ruut, conn_postgres):  
    # Limpiar la ventana principal
    for widget in ruut.winfo_children():
        widget.destroy()

    # Crear un nuevo marco dentro de root
    new_marco = tk.Frame(ruut)
    new_marco.pack(pady=10)
    new_marco["bg"]="#D4AF37"
    # Crear botones con comandos
    cliente_boton = tk.Button(new_marco, text="Clientes", font=("Arial", 12), command= lambda: agregar_clientepostgre(ruut, conn_postgres))
    cliente_boton.pack(pady=10)

    detalle_boton = tk.Button(new_marco, text="Detalles Venta", font=("Arial", 12), command= lambda: agregar_detallepostgre(ruut, conn_postgres))
    detalle_boton.pack(pady=10)

    producto_boton = tk.Button(new_marco, text="Productos", font=("Arial", 12), command= lambda: agregar_productopostgre(ruut, conn_postgres))
    producto_boton.pack(pady=10)

    venta_boton = tk.Button(new_marco, text="Ventas", font=("Arial", 12), command= lambda: agregar_ventaspostgre(ruut, conn_postgres))
    venta_boton.pack(pady=10)

    empleado_boton = tk.Button(new_marco, text="Empleados", font=("Arial", 12), command= lambda: agregar_empleadopostgre(ruut, conn_postgres))
    empleado_boton.pack(pady=10)

    volver_boton = tk.Button(new_marco, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexionpostgre(ruut, conn_postgres))
    volver_boton.pack(pady=10)


def modificarpostgre(ruut, conn_postgres):
 
    # Limpiar la ventana principal
    for widget in ruut.winfo_children():
        widget.destroy()

    # Crear un nuevo marco dentro de root
    new_marco = tk.Frame(ruut)
    new_marco.pack(pady=10)
    new_marco["bg"] = "#D4AF37"
   
    cliente_boton = tk.Button(new_marco, text="Clientes", font=("Arial", 12), command= lambda: modificar_clientepostgre(ruut, conn_postgres))  
    cliente_boton.pack(pady=10)

    producto_boton = tk.Button(new_marco, text="Productos", font=("Arial", 12), command= lambda: modificar_productopostgre(ruut, conn_postgres)) 
    producto_boton.pack(pady=10)

    empleado_boton = tk.Button(new_marco, text="Empleados", font=("Arial", 12), command= lambda: modificar_empleadopostgre(ruut, conn_postgres)) 
    empleado_boton.pack(pady=10)

    volver_boton = tk.Button(new_marco, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexionpostgre(ruut, conn_postgres))
    volver_boton.pack(pady=10)


def borrardatos_postgre(ruut, conn_postgres):  
    # Limpiar la ventana principal
    for widget in ruut.winfo_children():
        widget.destroy()

    # Crear un nuevo marco dentro de root
    new_marco = tk.Frame(ruut)
    new_marco.pack(pady=10)
    new_marco["bg"] = "#D4AF37"
   
    cliente_boton = tk.Button(new_marco, text="Clientes", font=("Arial", 12), command=lambda: borrar_clientepostgre(ruut, conn_postgres))  
    cliente_boton.pack(pady=10)

    detalle_boton = tk.Button(new_marco, text="Detalles Venta", font=("Arial", 12), command=lambda: borrar_detallepostgre(ruut, conn_postgres)) 
    detalle_boton.pack(pady=10)

    producto_boton = tk.Button(new_marco, text="Productos", font=("Arial", 12), command=lambda: borrar_productopostgre(ruut, conn_postgres)) 
    producto_boton.pack(pady=10)

    venta_boton = tk.Button(new_marco, text="Ventas", font=("Arial", 12), command=lambda: borrar_ventaspostgre(ruut, conn_postgres)) 
    venta_boton.pack(pady=10)

    empleado_boton = tk.Button(new_marco, text="Empleados", font=("Arial", 12), command=lambda: borrar_empleadopostgre(ruut, conn_postgres)) 
    empleado_boton.pack(pady=10)

    volver_boton = tk.Button(new_marco, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexionpostgre(ruut, conn_postgres))
    volver_boton.pack(pady=10)