import tkinter as tk
from tkinter import ttk
import psycopg2
from cerrarpo.closepostg import cerrar_conexionpostgre
from tkinter import messagebox
from datetime import datetime

def detalle_postgre(ruut, conn_postgres):
   
    try:
        # Consulta SQL para obtener los registros de la tabla 'categoria'
        SQL_QUERY = """
        SELECT *FROM detalles_venta;
        """

        # Crear un cursor y ejecutar la consulta
        cursor = conn_postgres.cursor()
        cursor.execute(SQL_QUERY)

        # Recuperar los nombres de las columnas de la tabla
        column_names = [desc[0] for desc in cursor.description]

        # Crear ventana para mostrar los datos
        ventana = tk.Toplevel(ruut)
        ventana.title("Tabla de Categorías")
        ventana.geometry("1000x600")

        # Crear Treeview
        tabla = ttk.Treeview(ventana, columns=column_names, show="headings")
        tabla.pack(fill=tk.BOTH, expand=True)

        # Configurar encabezados del Treeview
        for col in column_names:
            tabla.heading(col, text=col, anchor=tk.CENTER)
            tabla.column(col, anchor=tk.CENTER, width=100)

        # Insertar datos en el Treeview
        rows = cursor.fetchall()
        for row in rows:
            tabla.insert("", tk.END, values=row)

        # Cerrar el cursor
        cursor.close()

    except psycopg2.Error as e:
        print(f"Error al consultar la base de datos: {e}")


def insertar_detalle_venta(conn_postgres, detalle_id_entry, venta_id_entry, producto_id_entry, cantidad_entry, precio_unitario_entry):
    """
    Inserta un detalle de venta en la base de datos PostgreSQL.
    """
    # Obtener valores de los campos de entrada
    detalle_id = detalle_id_entry.get().strip()
    venta_id = venta_id_entry.get().strip()
    producto_id = producto_id_entry.get().strip()
    cantidad = cantidad_entry.get().strip()
    precio_unitario = precio_unitario_entry.get().strip()
    sub_total = int(cantidad) * int(precio_unitario)

    # Validar que no haya campos vacíos
    if not detalle_id or not venta_id or not producto_id or not cantidad or not precio_unitario or not sub_total:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    try:
        # Insertar datos en la base de datos
        cursor = conn_postgres.cursor()
        fecha_modificacion = datetime.now()
        SQL_INSERT = """
        INSERT INTO public.detalles_venta(
	 "Detalle_ID", "Venta_ID", "Producto_ID", "Cantidad", "Precio_Unitario", "Sub_Total", fecha_de_modificacion)
	 VALUES ( %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(SQL_INSERT, (
            detalle_id,
            venta_id,
            producto_id,
            cantidad,
            precio_unitario,
            str(sub_total),
            fecha_modificacion
        ))
        conn_postgres.commit()

        # Mensaje de éxito
        messagebox.showinfo("Éxito", f"Detalle de venta con ID '{detalle_id}' agregado correctamente.")

        # Limpiar los campos de entrada
        detalle_id_entry.delete(0, tk.END)
        venta_id_entry.delete(0, tk.END)
        producto_id_entry.delete(0, tk.END)
        cantidad_entry.delete(0, tk.END)
        precio_unitario_entry.delete(0, tk.END)
        

    except Exception as e:
        # Mensaje de error
        messagebox.showerror("Error", f"No se pudo agregar el detalle de venta. Detalles: {e}")
        conn_postgres.rollback()


def agregar_detallepostgre(ruut, conn_postgres):
    """
    Interfaz para agregar datos a la tabla 'detalles_venta' en PostgreSQL.
    """
    # Limpiar la ventana principal
    for widget in ruut.winfo_children():
        widget.destroy()

    # Crear un marco para el formulario
    frame = tk.Frame(ruut)
    frame.pack(pady=20)
    frame["bg"] = "#D4AF37"

    # Etiquetas y campos de entrada
    tk.Label(frame, text="Detalle ID", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    detalle_id_entry = tk.Entry(frame, font=("Arial", 12))
    detalle_id_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame, text="Venta ID", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
    venta_id_entry = tk.Entry(frame, font=("Arial", 12))
    venta_id_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(frame, text="Producto ID", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5)
    producto_id_entry = tk.Entry(frame, font=("Arial", 12))
    producto_id_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(frame, text="Cantidad", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5)
    cantidad_entry = tk.Entry(frame, font=("Arial", 12))
    cantidad_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(frame, text="Precio Unitario", font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=5)
    precio_unitario_entry = tk.Entry(frame, font=("Arial", 12))
    precio_unitario_entry.grid(row=4, column=1, padx=10, pady=5)


    # Botón para agregar el detalle de venta
    agregar_btn = tk.Button(
        frame,
        text="Agregar Detalle de Venta",
        font=("Arial", 12),
        command=lambda: insertar_detalle_venta(
            conn_postgres, 
            detalle_id_entry, 
            venta_id_entry, 
            producto_id_entry, 
            cantidad_entry, 
            precio_unitario_entry, 
        )
    )
    agregar_btn.grid(row=6, column=0, columnspan=2, pady=10)

    # Botón para salir
    salir_btn = tk.Button(frame, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexionpostgre(ruut, conn_postgres))
    salir_btn.grid(row=7, column=0, columnspan=2, pady=10)



def borrar_detallepostgre(ruut, conn_postgres):
    """
    Interfaz para eliminar todos los registros de un detalle de venta en específico usando su ID.
    """
    # Limpiar la ventana principal
    for widget in ruut.winfo_children():
        widget.destroy()

    # Crear un marco para el formulario
    frame = tk.Frame(ruut)
    frame.pack(pady=20)
    frame["bg"] = "#FF6347"

    # Etiquetas y campos de entrada
    tk.Label(frame, text="Detalle ID (a eliminar)", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    id_entry = tk.Entry(frame, font=("Arial", 12))
    id_entry.grid(row=0, column=1, padx=10, pady=5)

    # Función para eliminar detalle
    def eliminar_detalle():
        detalle_id = id_entry.get().strip()

        if not detalle_id:
            messagebox.showerror("Error", "El ID del detalle es obligatorio.")
            return

        try:
            # Ejecutar la eliminación en la base de datos
            cursor = conn_postgres.cursor()
            SQL_DELETE = """DELETE FROM public.detalles_venta WHERE "Detalle_ID" = %s;"""
            cursor.execute(SQL_DELETE, (detalle_id,))
            conn_postgres.commit()

            if cursor.rowcount == 0:
                messagebox.showwarning("Advertencia", f"No se encontró el detalle de venta con ID '{detalle_id}'.")
            else:
                messagebox.showinfo("Éxito", f"Detalle con ID '{detalle_id}' eliminado correctamente.")

            # Limpiar el campo de entrada
            id_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar detalle de venta. Detalles: {e}")
        finally:
            cursor.close()

    # Botón para eliminar detalle
    eliminar_btn = tk.Button(frame, text="Eliminar detalle", font=("Arial", 12), command=eliminar_detalle)
    eliminar_btn.grid(row=1, column=0, columnspan=2, pady=10)

    # Botón para volver al menú anterior
    volver_btn = tk.Button(frame, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexionpostgre(ruut, conn_postgres))
    volver_btn.grid(row=2, column=0, columnspan=2, pady=10)

