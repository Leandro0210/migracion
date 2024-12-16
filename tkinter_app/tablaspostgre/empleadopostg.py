import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import psycopg2
from datetime import datetime
from cerrarpo.closepostg import cerrar_conexionpostgre

def empleado_postgre(ruut, conn_postgres):
   
    try:
        # Consulta SQL para obtener los registros de la tabla 'categoria'
        SQL_QUERY = """
        SELECT *FROM empleado
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



def agregar_empleadopostgre(ruut, conn_postgres):
    """
    Interfaz para agregar datos a la tabla 'empleados'.
    """
    # Limpiar la ventana principal
    for widget in ruut.winfo_children():
        widget.destroy()

    # Crear un marco para el formulario
    frame = tk.Frame(ruut)
    frame.pack(pady=20)
    frame["bg"] = "#D4AF37"

    # Etiquetas y campos de entrada
    tk.Label(frame, text="Empleado ID", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    id_entry = tk.Entry(frame, font=("Arial", 12))
    id_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame, text="Nombre Empleado", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
    nombre_entry = tk.Entry(frame, font=("Arial", 12))
    nombre_entry.grid(row=1, column=1, padx=10, pady=5)

    # Función para insertar datos
    def insertar_empleado():
        empleado_id = id_entry.get().strip()
        nombre_emp = nombre_entry.get().strip()

        if not empleado_id or not nombre_emp:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            cursor = conn_postgres.cursor()
            fecha_modificacion = datetime.now()
            # Consulta SQL para insertar en la base de datos PostgreSQL
            SQL_INSERT = """ INSERT INTO public.empleado(
	     "Empleado_ID", "Nombre_Emp", fecha_de_modificacion)
	     VALUES (%s, %s, %s);     """
            cursor.execute(SQL_INSERT, (empleado_id, nombre_emp, fecha_modificacion))
            conn_postgres.commit()

            messagebox.showinfo("Éxito", f"Empleado '{nombre_emp}' agregado correctamente.")
            id_entry.delete(0, tk.END)
            nombre_entry.delete(0, tk.END)
            cursor.close()

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el empleado. Detalles: {e}")

    # Botón para agregar el empleado
    agregar_btn = tk.Button(frame, text="Agregar Empleado", font=("Arial", 12), command=insertar_empleado)
    agregar_btn.grid(row=2, column=0, columnspan=2, pady=10)

    # Botón para salir
    salir_btn = tk.Button(frame, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexionpostgre(ruut, conn_postgres))
    salir_btn.grid(row=3, column=0, columnspan=2, pady=10)


def modificar_empleadopostgre(ruut, conn_postgre):
    """
    Interfaz para modificar los datos de la tabla 'Empleado' en PostgreSQL.
    """
    # Limpiar la ventana principal
    for widget in ruut.winfo_children():
        widget.destroy()

    # Crear un marco para el formulario
    frame = tk.Frame(ruut)
    frame.pack(pady=20)
    frame["bg"] = "#87CEEB"

    # Etiquetas y campos de entrada
    tk.Label(frame, text="Empleado ID (a modificar)", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    id_entry = tk.Entry(frame, font=("Arial", 12))
    id_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame, text="Nuevo Nombre", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
    nombre_entry = tk.Entry(frame, font=("Arial", 12))
    nombre_entry.grid(row=1, column=1, padx=10, pady=5)

    # Función para modificar datos
    def actualizar_empleado():
        empleado_id = id_entry.get().strip()
        nuevo_nombre = nombre_entry.get().strip()

        if not empleado_id or not nuevo_nombre:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            # Actualizar datos en la base de datos
            cursor = conn_postgre.cursor()
            SQL_UPDATE = """
             UPDATE public.empleado
             SET "Nombre_Emp" = %s, fecha_de_modificacion = NOW()
             WHERE "Empleado_ID" = %s;

            """
            cursor.execute(SQL_UPDATE, (nuevo_nombre, empleado_id))
            conn_postgre.commit()

            if cursor.rowcount == 0:
                messagebox.showwarning("Advertencia", f"No se encontró el empleado con ID '{empleado_id}'.")
            else:
                messagebox.showinfo("Éxito", f"Empleado con ID '{empleado_id}' actualizado correctamente.")

            # Limpiar los campos de entrada
            id_entry.delete(0, tk.END)
            nombre_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el empleado. Detalles: {e}")
        finally:
            cursor.close()

    # Botón para actualizar los datos
    actualizar_btn = tk.Button(frame, text="Actualizar Empleado", font=("Arial", 12), command=actualizar_empleado)
    actualizar_btn.grid(row=2, column=0, columnspan=2, pady=10)

    # Botón para volver al menú anterior
    volver_btn = tk.Button(frame, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexionpostgre(ruut, conn_postgre))
    volver_btn.grid(row=3, column=0, columnspan=2, pady=10)


def borrar_empleadopostgre(ruut, conn_postgres):
    """
    Interfaz para eliminar todos los registros de un empleado en específico usando su ID.
    """
    # Limpiar la ventana principal
    for widget in ruut.winfo_children():
        widget.destroy()

    # Crear un marco para el formulario
    frame = tk.Frame(ruut)
    frame.pack(pady=20)
    frame["bg"] = "#FF6347"

    # Etiquetas y campos de entrada
    tk.Label(frame, text="Empleado ID (a eliminar)", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    id_entry = tk.Entry(frame, font=("Arial", 12))
    id_entry.grid(row=0, column=1, padx=10, pady=5)

    # Función para eliminar empleado
    def eliminar_empleado():
        empleado_id = id_entry.get().strip()

        if not empleado_id:
            messagebox.showerror("Error", "El ID del empleado es obligatorio.")
            return

        try:
            # Ejecutar la eliminación en la base de datos
            cursor = conn_postgres.cursor()
            SQL_DELETE = """DELETE FROM public.empleado WHERE "Empleado_ID" = %s;"""
            cursor.execute(SQL_DELETE, (empleado_id,))
            conn_postgres.commit()

            if cursor.rowcount == 0:
                messagebox.showwarning("Advertencia", f"No se encontró el empleado con ID '{empleado_id}'.")
            else:
                messagebox.showinfo("Éxito", f"Empleado con ID '{empleado_id}' eliminado correctamente.")

            # Limpiar el campo de entrada
            id_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el empleado. Detalles: {e}")
        finally:
            cursor.close()

    # Botón para eliminar empleado
    eliminar_btn = tk.Button(frame, text="Eliminar Empleado", font=("Arial", 12), command=eliminar_empleado)
    eliminar_btn.grid(row=1, column=0, columnspan=2, pady=10)

    # Botón para volver al menú anterior
    volver_btn = tk.Button(frame, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexionpostgre(ruut, conn_postgres))
    volver_btn.grid(row=2, column=0, columnspan=2, pady=10)