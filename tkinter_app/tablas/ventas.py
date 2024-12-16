import pyodbc
import tkinter as tk
from cerrar.close import cerrar_conexion
from tkinter import messagebox
from tkinter import ttk

def mostrar_ventas(conn):
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



def insertar_venta(conn, id_entrada, cliente_id_entrada, total_entrada, empleado_id_entrada, fecha_entrada):
    """
    Inserta una venta en la base de datos.
    """
    # Obtener valores de los campos de entrada
    venta_id = id_entrada.get().strip()
    cliente_id = cliente_id_entrada.get().strip()
    total = total_entrada.get().strip()
    empleado_id = empleado_id_entrada.get().strip()
    fecha = fecha_entrada.get().strip()

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
        id_entrada.delete(0, tk.END)
        cliente_id_entrada.delete(0, tk.END)
        total_entrada.delete(0, tk.END)
        empleado_id_entrada.delete(0, tk.END)
        fecha_entrada.delete(0, tk.END)

    except Exception as e:
        # Mensaje de error
        messagebox.showerror("Error", f"No se pudo agregar la venta. Detalles: {e}")


def agregar_venta(root, conn):
    """
    Interfaz para agregar datos a la tabla 'ventas'.
    """
    # Limpiar la ventana principal
    for widget in root.winfo_children():
        widget.destroy()

    # Crear un marco para el formulario
    marco = tk.Frame(root)
    marco.pack(pady=20)
    marco["bg"] = "#D4AF37"

    # Etiquetas y campos de entrada
    tk.Label(marco, text="Venta ID", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    id_entrada = tk.Entry(marco, font=("Arial", 12))
    id_entrada.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(marco, text="Cliente ID", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
    cliente_id_entrada = tk.Entry(marco, font=("Arial", 12))
    cliente_id_entrada.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(marco, text="Total", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5)
    total_entrada = tk.Entry(marco, font=("Arial", 12))
    total_entrada.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(marco, text="Empleado ID", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5)
    empleado_id_entrada = tk.Entry(marco, font=("Arial", 12))
    empleado_id_entrada.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(marco, text="Fecha (YYYY-MM-DD)", font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=5)
    fecha_entrada = tk.Entry(marco, font=("Arial", 12))
    fecha_entrada.grid(row=4, column=1, padx=10, pady=5)

    # Botón para agregar la venta
    agregar_boton = tk.Button(
        marco,
        text="Agregar Venta",
        font=("Arial", 12),
        command=lambda: insertar_venta(conn, id_entrada, cliente_id_entrada, total_entrada, empleado_id_entrada, fecha_entrada)
    )
    agregar_boton.grid(row=5, column=0, columnspan=2, pady=10)

    # Botón para salir
    salir_boton = tk.Button(marco, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexion(root, conn))
    salir_boton.grid(row=6, column=0, columnspan=2, pady=10)



def eliminar_venta(root, conn, venta_id_entrada):
    """
    Función para eliminar un registro de la tabla 'Ventas' dado su Venta_ID.
    """
    venta_id = venta_id_entrada.get().strip()

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
        venta_id_entrada.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar la venta. Detalles: {e}")

def borrar_venta(root, conn):
    """
    Interfaz para eliminar un registro de la tabla 'Ventas' dado su Venta_ID.
    """
    # Limpiar la ventana principal
    for widget in root.winfo_children():
        widget.destroy()

    # Crear un marco para el formulario
    marco = tk.Frame(root)
    marco.pack(pady=20)
    marco["bg"] = "#FFC0CB"

    # Etiquetas y campos de entrada
    tk.Label(marco, text="Venta ID (a eliminar)", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    venta_id_entrada = tk.Entry(marco, font=("Arial", 12))
    venta_id_entrada.grid(row=0, column=1, padx=10, pady=5)

    # Botón para eliminar el registro
    eliminar_boton = tk.Button(marco, text="Eliminar Venta", font=("Arial", 12), 
                               command=lambda: eliminar_venta(root, conn, venta_id_entrada))
    eliminar_boton.grid(row=1, column=0, columnspan=2, pady=10)

    # Botón para volver al menú anterior
    volver_boton = tk.Button(marco, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexion(root, conn))
    volver_boton.grid(row=2, column=0, columnspan=2, pady=10)
