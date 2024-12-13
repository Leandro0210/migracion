import pyodbc
import tkinter as tk
from cerrar.close import cerrar_conexion
from tkinter import messagebox
from tkinter import ttk

def mues_ven(conn):
    """
    Muestra los registros de la tabla 'ventas' usando la conexión proporcionada en un Treeview.
    """
    try:
        # Define la consulta SQL
        SQL_QUERY = "SELECT * from ventas"  # Ajusta las columnas según tu tabla

        # Crear un cursor y ejecutar la consulta
        cursor = conn.cursor()
        cursor.execute(SQL_QUERY)

        # Recuperar los nombres de las columnas de la tabla
        column_names = [desc[0] for desc in cursor.description]

        # Crear ventana de Tkinter para mostrar los datos
        ventana = tk.Tk()
        ventana.title("Ventas")
        ventana.geometry("600x400")
        ventana.iconbitmap("logo.ico")

        # Crear Treeview con las columnas necesarias
        tabla = ttk.Treeview(ventana, columns=column_names, show="headings")
        tabla.pack(fill=tk.BOTH, expand=True)

        # Configurar encabezados del Treeview
        for col in column_names:
            tabla.heading(col, text=col, anchor=tk.CENTER)
            tabla.column(col, anchor=tk.CENTER, width=100)

        # Insertar datos en el Treeview
        rows = cursor.fetchall()
        for row in rows:
            tabla.insert("", tk.END, values=row)  # Insertar fila en la tabla

        # Cerrar el cursor
        cursor.close()

       

    except pyodbc.Error as e:
        print(f"Error al consultar la base de datos: {e}")



def insertar_venta(conn, id_entry, cliente_id_entry, total_entry, empleado_id_entry, fecha_entry):
    """
    Inserta una venta en la base de datos.
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
        cursor = conn.cursor()
        SQL_INSERT = """
        INSERT INTO ventas (Venta_ID, Cliente_ID, Total, Empleado_ID, Fecha)
        VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(SQL_INSERT, (venta_id, cliente_id, float(total), empleado_id, fecha))
        conn.commit()

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


def agre_ven(root, conn):
    """
    Interfaz para agregar datos a la tabla 'ventas'.
    """
    # Limpiar la ventana principal
    for widget in root.winfo_children():
        widget.destroy()

    # Crear un marco para el formulario
    frame = tk.Frame(root)
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
        command=lambda: insertar_venta(conn, id_entry, cliente_id_entry, total_entry, empleado_id_entry, fecha_entry)
    )
    agregar_btn.grid(row=5, column=0, columnspan=2, pady=10)

    # Botón para salir
    salir_btn = tk.Button(frame, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexion(root, conn))
    salir_btn.grid(row=6, column=0, columnspan=2, pady=10)



def del_ven(root, conn):
    """
    Interfaz para eliminar un registro de la tabla 'Ventas' dado su Venta_ID.
    """
    # Limpiar la ventana principal
    for widget in root.winfo_children():
        widget.destroy()

    # Crear un marco para el formulario
    frame = tk.Frame(root)
    frame.pack(pady=20)
    frame["bg"] = "#FFC0CB"

    # Etiquetas y campos de entrada
    tk.Label(frame, text="Venta ID (a eliminar)", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    venta_id_entry = tk.Entry(frame, font=("Arial", 12))
    venta_id_entry.grid(row=0, column=1, padx=10, pady=5)

    # Función para eliminar un registro
    def eliminar_venta():
        venta_id = venta_id_entry.get().strip()

        if not venta_id:
            messagebox.showerror("Error", "El ID de la venta es obligatorio.")
            return

        try:
            # Eliminar registro en la base de datos
            cursor = conn.cursor()
            SQL_DELETE = "DELETE FROM Ventas WHERE Venta_ID = ?"
            cursor.execute(SQL_DELETE, (venta_id,))
            conn.commit()

            if cursor.rowcount == 0:
                messagebox.showwarning("Advertencia", f"No se encontró la venta con ID '{venta_id}'.")
            else:
                messagebox.showinfo("Éxito", f"Venta con ID '{venta_id}' eliminada correctamente.")

            # Limpiar el campo de entrada
            venta_id_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar la venta. Detalles: {e}")

    # Botón para eliminar el registro
    eliminar_btn = tk.Button(frame, text="Eliminar Venta", font=("Arial", 12), command=eliminar_venta)
    eliminar_btn.grid(row=1, column=0, columnspan=2, pady=10)

    # Botón para volver al menú anterior
    volver_btn = tk.Button(frame, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexion(root, conn))
    volver_btn.grid(row=2, column=0, columnspan=2, pady=10)
