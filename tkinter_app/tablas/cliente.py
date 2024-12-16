import pyodbc
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from cerrar.close import cerrar_conexion

def mostrar_clientes(conn):
    """
    Muestra los registros de la tabla 'cliente' en una tabla gráfica (Treeview) usando la conexión proporcionada.
    """
    try:
        # Define la consulta SQL con las columnas necesarias
        SQL_QUERY = "SELECT * from cliente"  # Ajusta las columnas según tu tabla

        # Crear un cursor y ejecutar la consulta
        cursor = conn.cursor()
        cursor.execute(SQL_QUERY)

        # Recuperar los nombres de las columnas de la tabla
        column_names = [desc[0] for desc in cursor.description]

        # Crear ventana de Tkinter para mostrar los datos
        ventana = tk.Tk()
        ventana.title("Tabla de Clientes")
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
            # Concatenar el nombre y apellido si es necesario
            nombre_completo = f"{row[1]}"  
            telefono = row[2] 
            correo = row[3]  
            tabla.insert("", tk.END, values=(row[0], nombre_completo, telefono, correo))  # Insertar fila en la tabla

        # Cerrar el cursor
        cursor.close()


    except pyodbc.Error as e:
        print(f"Error al consultar la base de datos: {e}")


def insertar_cliente(conn, id_entrada, nombre_entrada, telefono_entrada, core_entrada):
    """
    Inserta un cliente en la base de datos.
    """
    # Obtener valores de los campos de entrada
    cliente_id = id_entrada.get().strip()
    nombre = nombre_entrada.get().strip()
    telefono = telefono_entrada.get().strip()
    correo = core_entrada.get().strip()

    # Validar que no haya campos vacíos
    if not cliente_id or not nombre or not telefono or not correo:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    try:
        # Insertar datos en la base de datos
        cursor = conn.cursor()
        SQL_INSERT = "INSERT INTO cliente (Cliente_ID, Nombre, Telefono, Correo) VALUES (?, ?, ?, ?)"
        cursor.execute(SQL_INSERT, (cliente_id, nombre, telefono, correo))
        conn.commit()

        # Mensaje de éxito
        messagebox.showinfo("Éxito", f"Cliente '{nombre}' agregado correctamente.")

        # Limpiar los campos de entrada
        id_entrada.delete(0, tk.END)
        nombre_entrada.delete(0, tk.END)
        telefono_entrada.delete(0, tk.END)
        core_entrada.delete(0, tk.END)

    except Exception as e:
        # Mensaje de error
        messagebox.showerror("Error", f"No se pudo agregar el cliente. Detalles: {e}")


def agregar_cliente(root, conn):
    """
    Interfaz para agregar datos a la tabla 'Cliente'.
    """
    # Limpiar la ventana principal
    for widget in root.winfo_children():
        widget.destroy()

    # Crear un marco para el formulario
    marco = tk.Frame(root)
    marco.pack(pady=20)
    marco["bg"]="#D4AF37"
    # Etiquetas y campos de entrada
    tk.Label(marco, text="Cliente ID", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    id_entrada = tk.Entry(marco, font=("Arial", 12))
    id_entrada.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(marco, text="Nombre Cliente", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
    nombre_entrada = tk.Entry(marco, font=("Arial", 12))
    nombre_entrada.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(marco, text="Número Telefónico", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5)
    telefono_entrada = tk.Entry(marco, font=("Arial", 12))
    telefono_entrada.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(marco, text="Correo Electrónico", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5)
    core_entrada = tk.Entry(marco, font=("Arial", 12))
    core_entrada.grid(row=3, column=1, padx=10, pady=5)

    # Botón para agregar el cliente
    agregar_boton = tk.Button(
        marco,
        text="Agregar Cliente",
        font=("Arial", 12),
        command=lambda: insertar_cliente(conn, id_entrada, nombre_entrada, telefono_entrada, core_entrada)
    )
    agregar_boton.grid(row=4, column=0, columnspan=2, pady=10)

    # Botón para salir
    salir_boton = tk.Button(marco, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexion(root, conn))
    salir_boton.grid(row=5, column=0, columnspan=2, pady=10)


def modificar_cliente(root, conn):
    """
    Interfaz para modificar los datos de la tabla 'Cliente' (Teléfono y Correo).
    """
    # Limpiar la ventana principal
    for widget in root.winfo_children():
        widget.destroy()

    # Crear un marco para el formulario
    marco = tk.Frame(root)
    marco.pack(pady=20)
    marco["bg"] = "#87CEEB"

    # Etiquetas y campos de entrada
    tk.Label(marco, text="Cliente ID (a modificar)", font=("Arial", 12)).grid(row=0, column=0, padx=15, pady=10)
    id_entrada = tk.Entry(marco, font=("Arial", 12))
    id_entrada.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(marco, text="Nuevo Teléfono (opcional)", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
    telefono_entrada = tk.Entry(marco, font=("Arial", 12))
    telefono_entrada.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(marco, text="Nuevo Correo (opcional)", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5)
    correo_entrada = tk.Entry(marco, font=("Arial", 12))
    correo_entrada.grid(row=2, column=1, padx=10, pady=5)


    # Botón para actualizar los datos
    actualizar_boton = tk.Button(marco, text="Actualizar Cliente", font=("Arial", 12), command=lambda: actualizar_cliente(conn, id_entrada, telefono_entrada, correo_entrada))
    actualizar_boton.grid(row=3, column=0, columnspan=2, pady=10)

    # Botón para volver al menú anterior
    volver_boton = tk.Button(marco, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexion(root, conn))
    volver_boton.grid(row=4, column=0, columnspan=2, pady=10)


# Función para modificar datos
def actualizar_cliente(conn, id_entrada, telefono_entrada, correo_entrada):
    cliente_id = id_entrada.get().strip()
    nuevo_telefono = telefono_entrada.get().strip()
    nuevo_correo = correo_entrada.get().strip()

    if not cliente_id:
            messagebox.showerror("Error", "El ID del cliente es obligatorio.")
            return

    try:
     # Construcción dinámica de la consulta
     parametros = []
     if nuevo_telefono:
         parametros.append(f"Telefono = '{nuevo_telefono}'")
     if nuevo_correo:
         parametros.append(f"Correo = '{nuevo_correo}'")

     if not parametros:
         messagebox.showerror("Error", "Debe ingresar al menos un campo para actualizar.")
         return

     # Construye la consulta SQL
     set_clause = ", ".join(parametros)
     SQL_UPDATE = f"UPDATE Cliente SET {set_clause} WHERE Cliente_ID = ?"

     # Ejecuta la consulta
     cursor = conn.cursor()
     cursor.execute(SQL_UPDATE, (cliente_id,))
     conn.commit()

     if cursor.rowcount == 0:
         messagebox.showwarning("Advertencia", f"No se encontró el cliente con ID '{cliente_id}'.")
     else:
         messagebox.showinfo("Éxito", f"Cliente con ID '{cliente_id}' actualizado correctamente.")
            
     # Limpiar los campos de entrada
     id_entrada.delete(0, tk.END)
     telefono_entrada.delete(0, tk.END)
     correo_entrada.delete(0, tk.END)
    except Exception as e:
         messagebox.showerror("Error", f"No se pudo actualizar el cliente. Detalles: {e}")



def borrar_cliente(root, conn):
    """
    Interfaz para eliminar todos los registros de un cliente en específico usando su ID.
    """
    # Limpiar la ventana principal
    for widget in root.winfo_children():
        widget.destroy()

    # Crear un marco para el formulario
    marco = tk.Frame(root)
    marco.pack(pady=20)
    marco["bg"] = "#FF6347"

    # Etiquetas y campos de entrada
    tk.Label(marco, text="Cliente ID (a eliminar)", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    id_entrada = tk.Entry(marco, font=("Arial", 12))
    id_entrada.grid(row=0, column=1, padx=10, pady=5)

    # Función para eliminar cliente
    

    # Botón para eliminar cliente
    eliminar_boton = tk.Button(marco, text="Eliminar Cliente", font=("Arial", 12), command=lambda: eliminar_cliente(conn, id_entrada))
    eliminar_boton.grid(row=1, column=0, columnspan=2, pady=10)

    # Botón para volver al menú anterior
    volver_boton = tk.Button(marco, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexion(root, conn))
    volver_boton.grid(row=2, column=0, columnspan=2, pady=10)


def eliminar_cliente(conn, id_entrada):
    cliente_id = id_entrada.get().strip()  
    if not cliente_id:
        messagebox.showerror("Error", "El ID del cliente es obligatorio.")
        return

    try:
        
        cursor = conn.cursor()
        SQL_DELETE = "DELETE FROM Cliente WHERE Cliente_ID = ?"
        cursor.execute(SQL_DELETE, (cliente_id,))
        conn.commit()

        if cursor.rowcount == 0:
            messagebox.showwarning("Advertencia", f"No se encontró el cliente con ID '{cliente_id}'.")
        else:
            messagebox.showinfo("Éxito", f"Cliente con ID '{cliente_id}' eliminado correctamente.")

        id_entrada.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar el cliente. Detalles: {e}")