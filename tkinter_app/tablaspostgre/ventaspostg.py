import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import psycopg2
from datetime import datetime
from cerrarpo.closepostg import cerrar_conexionpostgre

def ventas_postgre(ruut, conn_postgres):
   
    try:
        # Consulta SQL para obtener los registros de la tabla 'categoria'
        SQL_QUERY = """
        SELECT *FROM ventas
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


def insertar_venta(conn_postgres, id_entry, cliente_id_entry, total_entry, empleado_id_entry, fecha_entry):
    """
    Inserta una venta en la base de datos PostgreSQL.
    """
    # Obtener valores de los campos de entrada
    venta_id = id_entry.get().strip()
    cliente_id = cliente_id_entry.get().strip()
    total = total_entry.get().strip()
    empleado_id = empleado_id_entry.get().strip()
    fecha = fecha_entry.get().strip()

    # Validar que no haya campos vacíos
    if not venta_id or not cliente_id or not total or not empleado_id or not fecha:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    try:
        # Insertar datos en la base de datos
        cursor = conn_postgres.cursor()
        fecha_modificacion = datetime.now()
        SQL_INSERT = """
        INSERT INTO public.ventas(
	 "Venta_ID", "Cliente_ID", "Total", "Empleado_ID", "Fecha", fecha_de_modificacion)
	 VALUES (%s, %s, %s, %s, %s, %s);
        """
        cursor.execute(SQL_INSERT, (venta_id, cliente_id, total, empleado_id, fecha, fecha_modificacion))
        conn_postgres.commit()

        # Mensaje de éxito
        messagebox.showinfo("Éxito", f"Venta con ID '{venta_id}' agregada correctamente.")

        # Limpiar los campos de entrada
        id_entry.delete(0, tk.END)
        cliente_id_entry.delete(0, tk.END)
        total_entry.delete(0, tk.END)
        empleado_id_entry.delete(0, tk.END)
        fecha_entry.delete(0, tk.END)

    except Exception as e:
        # Mensaje de error
        messagebox.showerror("Error", f"No se pudo agregar la venta. Detalles: {e}")


def agregar_ventaspostgre(ruut, conn_postgres):
    """
    Interfaz para agregar datos a la tabla 'ventas' en PostgreSQL.
    """
    # Limpiar la ventana principal
    for widget in ruut.winfo_children():
        widget.destroy()

    # Crear un marco para el formulario
    frame = tk.Frame(ruut)
    frame.pack(pady=20)
    frame["bg"] = "#D4AF37"

    # Etiquetas y campos de entrada
    tk.Label(frame, text="Venta ID", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    id_entry = tk.Entry(frame, font=("Arial", 12))
    id_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame, text="Cliente ID", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
    cliente_id_entry = tk.Entry(frame, font=("Arial", 12))
    cliente_id_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(frame, text="Total", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5)
    total_entry = tk.Entry(frame, font=("Arial", 12))
    total_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(frame, text="Empleado ID", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5)
    empleado_id_entry = tk.Entry(frame, font=("Arial", 12))
    empleado_id_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(frame, text="Fecha (YYYY-MM-DD)", font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=5)
    fecha_entry = tk.Entry(frame, font=("Arial", 12))
    fecha_entry.grid(row=4, column=1, padx=10, pady=5)

    # Botón para agregar la venta
    agregar_btn = tk.Button(
        frame,
        text="Agregar Venta",
        font=("Arial", 12),
        command=lambda: insertar_venta(conn_postgres, id_entry, cliente_id_entry, total_entry, empleado_id_entry, fecha_entry)
    )
    agregar_btn.grid(row=5, column=0, columnspan=2, pady=10)

    # Botón para salir
    salir_btn = tk.Button(frame, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexionpostgre(ruut, conn_postgres))
    salir_btn.grid(row=6, column=0, columnspan=2, pady=10)


def borrar_ventaspostgre(ruut, conn_postgres): 
    """
    Interfaz para eliminar todos los registros de una venta en específico usando su ID.
    """
    # Limpiar la ventana principal
    for widget in ruut.winfo_children():
        widget.destroy()

    # Crear un marco para el formulario
    frame = tk.Frame(ruut)
    frame.pack(pady=20)
    frame["bg"] = "#FF6347"

    # Etiquetas y campos de entrada
    tk.Label(frame, text="Venta ID (a eliminar)", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    id_entry = tk.Entry(frame, font=("Arial", 12))
    id_entry.grid(row=0, column=1, padx=10, pady=5)

    # Función para eliminar venta
    def eliminar_venta():
        venta_id = id_entry.get().strip()

        if not venta_id:
            messagebox.showerror("Error", "El ID de la venta es obligatorio.")
            return

        try:
            # Ejecutar la eliminación en la base de datos
            cursor = conn_postgres.cursor()
            SQL_DELETE = """DELETE FROM public.ventas WHERE "Venta_ID" = %s;"""
            cursor.execute(SQL_DELETE, (venta_id,))
            conn_postgres.commit()

            if cursor.rowcount == 0:
                messagebox.showwarning("Advertencia", f"No se encontró la venta con ID '{venta_id}'.")
            else:
                messagebox.showinfo("Éxito", f"Venta con ID '{venta_id}' eliminada correctamente.")

            # Limpiar el campo de entrada
            id_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar la venta. Detalles: {e}")
        finally:
            cursor.close()

    # Botón para eliminar venta
    eliminar_btn = tk.Button(frame, text="Eliminar Venta", font=("Arial", 12), command=eliminar_venta)
    eliminar_btn.grid(row=1, column=0, columnspan=2, pady=10)

    # Botón para volver al menú anterior
    volver_btn = tk.Button(frame, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexionpostgre(ruut, conn_postgres))
    volver_btn.grid(row=2, column=0, columnspan=2, pady=10)
