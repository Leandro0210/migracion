import tkinter as tk
from tkinter import ttk
import pyodbc

def mostrar_categoria(conn):
    """
    Muestra los registros de la tabla 'categoria' en una tabla gráfica (Treeview) usando la conexión proporcionada.
    """
    try:
        # Define la consulta SQL
        SQL_QUERY = "SELECT * FROM categoria"

        # Crear un cursor y ejecutar la consulta
        cursor = conn.cursor()
        cursor.execute(SQL_QUERY)

        # Recuperar los nombres de las columnas de la tabla
        column_names = [desc[0] for desc in cursor.description]

        # Crear ventana de Tkinter para mostrar los datos
        ventana = tk.Tk()
        ventana.title("Tabla de Categorías")
        ventana.geometry("600x400")

        # Crear Treeview
        tabla = ttk.Treeview(ventana, columns=column_names, show="headings")
        tabla.pack(fill=tk.BOTH, expand=True)

        # Configurar encabezados del Treeview
        for col in column_names:
            tabla.heading(col, text=col, anchor=tk.CENTER)
            tabla.column(col, anchor=tk.CENTER, width=100)

        # Insertar datos en el Treeview
        filas = cursor.fetchall()
        for row in filas:
            tabla.insert("", tk.END, values=row)

        # Cerrar el cursor
        cursor.close()


    except pyodbc.Error as e:
        print(f"Error al consultar la base de datos: {e}")
