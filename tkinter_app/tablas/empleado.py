import pyodbc
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from cerrar.close import cerrar_conexion
def mues_emp(conn):
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

def agre_emp(root, conn):
    """
    Interfaz para agregar datos a la tabla 'empleados'.
    """
    # Limpiar la ventana principal
    for widget in root.winfo_children():
        widget.destroy()

    # Crear un marco para el formulario
    frame = tk.Frame(root)
    frame.pack(pady=20)
    frame["bg"]="#D4AF37"
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
            cursor = conn.cursor()
            SQL_INSERT = "INSERT INTO Empleado (empleado_ID, Nombre_emp) VALUES (?, ?)"
            cursor.execute(SQL_INSERT, (empleado_id, nombre_emp))
            conn.commit()

            messagebox.showinfo("Éxito", f"Empleado '{nombre_emp}' agregado correctamente.")
            id_entry.delete(0, tk.END)
            nombre_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el empleado. Detalles: {e}")

    # Botón para agregar el empleado
    agregar_btn = tk.Button(frame, text="Agregar Empleado", font=("Arial", 12), command=insertar_empleado)
    agregar_btn.grid(row=2, column=0, columnspan=2, pady=10)
    # Botón para salir
    salir_btn = tk.Button(frame, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexion(root, conn))
    salir_btn.grid(row=3, column=0, columnspan=2, pady=10)
  

def mod_emp(root, conn):
    """
    Interfaz para modificar los datos de la tabla 'Empleado'.
    """
    # Limpiar la ventana principal
    for widget in root.winfo_children():
        widget.destroy()

    # Crear un marco para el formulario
    frame = tk.Frame(root)
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
            cursor = conn.cursor()
            SQL_UPDATE = "UPDATE Empleado SET Nombre_emp = ? WHERE empleado_ID = ?"
            cursor.execute(SQL_UPDATE, (nuevo_nombre, empleado_id))
            conn.commit()

            if cursor.rowcount == 0:
                messagebox.showwarning("Advertencia", f"No se encontró el empleado con ID '{empleado_id}'.")
            else:
                messagebox.showinfo("Éxito", f"Empleado con ID '{empleado_id}' actualizado correctamente.")
            
            # Limpiar los campos de entrada
            id_entry.delete(0, tk.END)
            nombre_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el empleado. Detalles: {e}")

    # Botón para actualizar los datos
    actualizar_btn = tk.Button(frame, text="Actualizar Empleado", font=("Arial", 12), command=actualizar_empleado)
    actualizar_btn.grid(row=2, column=0, columnspan=2, pady=10)

    # Botón para volver al menú anterior
    volver_btn = tk.Button(frame, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexion(root, conn))
    volver_btn.grid(row=3, column=0, columnspan=2, pady=10)
    

def del_emp(root, conn):
    """
    Interfaz para eliminar un registro de la tabla 'Empleado' dado su Empleado_ID.
    """
    # Limpiar la ventana principal
    for widget in root.winfo_children():
        widget.destroy()

    # Crear un marco para el formulario
    frame = tk.Frame(root)
    frame.pack(pady=20)
    frame["bg"] = "#FFD700"

    # Etiquetas y campos de entrada
    tk.Label(frame, text="Empleado ID (a eliminar)", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    empleado_id_entry = tk.Entry(frame, font=("Arial", 12))
    empleado_id_entry.grid(row=0, column=1, padx=10, pady=5)

    # Función para eliminar un registro
    def eliminar_empleado():
        empleado_id = empleado_id_entry.get().strip()

        if not empleado_id:
            messagebox.showerror("Error", "El ID del empleado es obligatorio.")
            return

        try:
            # Eliminar registro en la base de datos
            cursor = conn.cursor()
            SQL_DELETE = "DELETE FROM Empleado WHERE Empleado_ID = ?"
            cursor.execute(SQL_DELETE, (empleado_id,))
            conn.commit()

            if cursor.rowcount == 0:
                messagebox.showwarning("Advertencia", f"No se encontró el empleado con ID '{empleado_id}'.")
            else:
                messagebox.showinfo("Éxito", f"Empleado con ID '{empleado_id}' eliminado correctamente.")

            # Limpiar el campo de entrada
            empleado_id_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el empleado. Detalles: {e}")

    # Botón para eliminar el registro
    eliminar_btn = tk.Button(frame, text="Eliminar Empleado", font=("Arial", 12), command=eliminar_empleado)
    eliminar_btn.grid(row=1, column=0, columnspan=2, pady=10)

    # Botón para volver al menú anterior
    volver_btn = tk.Button(frame, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexion(root, conn))
    volver_btn.grid(row=2, column=0, columnspan=2, pady=10)
