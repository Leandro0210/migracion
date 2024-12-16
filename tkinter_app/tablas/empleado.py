import pyodbc
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from cerrar.close import cerrar_conexion

def mostrar_empleados(conn):
    """
    Muestra los registros de la tabla 'Empleado' usando la conexión proporcionada.
    """
    try:
        # Define la consulta SQL
        SQL_QUERY = "SELECT * FROM empleado"

        # Crear un cursor y ejecutar la consulta
        cursor = conn.cursor()
        cursor.execute(SQL_QUERY)

        # Recuperar los nombres de las columnas de la tabla
        column_names = [desc[0] for desc in cursor.description]

        # Crear ventana de Tkinter para mostrar los datos
        ventana = tk.Tk()
        ventana.title("Tabla de Empleados")
        ventana.geometry("600x400")
        ventana.iconbitmap("logo.ico")

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
            clean_row = tuple(str(value).strip() for value in row)  # Limpia espacios en blanco
            tabla.insert("", tk.END, values=clean_row)

        # Cerrar el cursor
        cursor.close()


    except pyodbc.Error as e:
        print(f"Error al consultar la base de datos: {e}")


def insertar_empleado(conn, id_entrada, nombre_entrada):
    empleado_id = id_entrada.get().strip()
    nombre_empleado = nombre_entrada.get().strip()

    if not empleado_id or not nombre_empleado:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    try:
        cursor = conn.cursor()
        SQL_INSERT = "INSERT INTO Empleado (empleado_ID, Nombre_emp) VALUES (?, ?)"
        cursor.execute(SQL_INSERT, (empleado_id, nombre_empleado))
        conn.commit()

        messagebox.showinfo("Éxito", f"Empleado '{nombre_empleado}' agregado correctamente.")
        id_entrada.delete(0, tk.END)
        nombre_entrada.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo agregar el empleado. Detalles: {e}")

def actualizar_empleado(conn, id_entrada, nombre_entrada):
    empleado_id = id_entrada.get().strip()
    nuevo_nombre = nombre_entrada.get().strip()

    if not empleado_id or not nuevo_nombre:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    try:
        cursor = conn.cursor()
        SQL_UPDATE = "UPDATE Empleado SET Nombre_emp = ? WHERE empleado_ID = ?"
        cursor.execute(SQL_UPDATE, (nuevo_nombre, empleado_id))
        conn.commit()

        if cursor.rowcount == 0:
            messagebox.showwarning("Advertencia", f"No se encontró el empleado con ID '{empleado_id}'.")
        else:
            messagebox.showinfo("Éxito", f"Empleado con ID '{empleado_id}' actualizado correctamente.")

        id_entrada.delete(0, tk.END)
        nombre_entrada.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar el empleado. Detalles: {e}")

def eliminar_empleado(conn, empleado_id_entrada):
    empleado_id = empleado_id_entrada.get().strip()

    if not empleado_id:
        messagebox.showerror("Error", "El ID del empleado es obligatorio.")
        return

    try:
        cursor = conn.cursor()
        SQL_DELETE = "DELETE FROM Empleado WHERE Empleado_ID = ?"
        cursor.execute(SQL_DELETE, (empleado_id,))
        conn.commit()

        if cursor.rowcount == 0:
            messagebox.showwarning("Advertencia", f"No se encontró el empleado con ID '{empleado_id}'.")
        else:
            messagebox.showinfo("Éxito", f"Empleado con ID '{empleado_id}' eliminado correctamente.")

        empleado_id_entrada.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar el empleado. Detalles: {e}")

def agregar_empleado(root, conn):
    for widget in root.winfo_children():
        widget.destroy()

    marco = tk.Frame(root)
    marco.pack(pady=20)
    marco["bg"] = "#D4AF37"

    tk.Label(marco, text="Empleado ID", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    id_entrada = tk.Entry(marco, font=("Arial", 12))
    id_entrada.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(marco, text="Nombre Empleado", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
    nombre_entrada = tk.Entry(marco, font=("Arial", 12))
    nombre_entrada.grid(row=1, column=1, padx=10, pady=5)

    agregar_boton = tk.Button(marco, text="Agregar Empleado", font=("Arial", 12), command=lambda: insertar_empleado(conn, id_entrada, nombre_entrada))
    agregar_boton.grid(row=2, column=0, columnspan=2, pady=10)

    salir_boton = tk.Button(marco, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexion(root, conn))
    salir_boton.grid(row=3, column=0, columnspan=2, pady=10)

def modificar_empleado(root, conn):
    for widget in root.winfo_children():
        widget.destroy()

    marco = tk.Frame(root)
    marco.pack(pady=20)
    marco["bg"] = "#87CEEB"

    tk.Label(marco, text="Empleado ID (a modificar)", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    id_entrada = tk.Entry(marco, font=("Arial", 12))
    id_entrada.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(marco, text="Nuevo Nombre", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
    nombre_entrada = tk.Entry(marco, font=("Arial", 12))
    nombre_entrada.grid(row=1, column=1, padx=10, pady=5)

    actualizar_boton = tk.Button(marco, text="Actualizar Empleado", font=("Arial", 12), command=lambda: actualizar_empleado(conn, id_entrada, nombre_entrada))
    actualizar_boton.grid(row=2, column=0, columnspan=2, pady=10)

    volver_boton = tk.Button(marco, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexion(root, conn))
    volver_boton.grid(row=3, column=0, columnspan=2, pady=10)

def borrar_empleado(root, conn):
    for widget in root.winfo_children():
        widget.destroy()

    marco = tk.Frame(root)
    marco.pack(pady=20)
    marco["bg"] = "#FFD700"

    tk.Label(marco, text="Empleado ID (a eliminar)", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    empleado_id_entrada = tk.Entry(marco, font=("Arial", 12))
    empleado_id_entrada.grid(row=0, column=1, padx=10, pady=5)

    eliminar_boton = tk.Button(marco, text="Eliminar Empleado", font=("Arial", 12), command=lambda: eliminar_empleado(conn, empleado_id_entrada))
    eliminar_boton.grid(row=1, column=0, columnspan=2, pady=10)

    volver_boton = tk.Button(marco, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexion(root, conn))
    volver_boton.grid(row=2, column=0, columnspan=2, pady=10)
