import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import psycopg2
from datetime import datetime
from cerrarpo.closepostg import cerrar_conexionpostgre

def cliente_postgre(ruut, conn_postgres):
   
    try:
        # Consulta SQL para obtener los registros de la tabla 'categoria'
        SQL_QUERY = """
        SELECT *FROM cliente;
        """

        # Crear un cursor y ejecutar la consulta
        cursor = conn_postgres.cursor()
        cursor.execute(SQL_QUERY)

        # Recuperar los nombres de las columnas de la tabla
        column_names = [desc[0] for desc in cursor.description]

        # Crear ventana para mostrar los datos
        ventana = tk.Toplevel(ruut)
        ventana.title("Tabla de Categorías")
        ventana.geometry("800x600")

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


def insertar_cliente(conn_postgres, id_entry, nombre_entry, telefono_entry, core_entry):
    """
    Inserta un cliente en la base de datos PostgreSQL.
    """
    # Obtener valores de los campos de entrada
    cliente_id = id_entry.get().strip()
    nombre = nombre_entry.get().strip()
    telefono = telefono_entry.get().strip()
    correo = core_entry.get().strip()

    # Validar que no haya campos vacíos
    if not cliente_id or not nombre or not telefono or not correo:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    try:
        # Insertar datos en la base de datos
        cursor = conn_postgres.cursor()
        
        # Enviar fecha de modificación explícitamente con datetime.now()
        fecha_modificacion = datetime.now()

        SQL_INSERT = """
           INSERT INTO public.cliente(
	 "Cliente_ID", "Nombre", "Telefono", "Correo", fecha_de_modificacion)
	 VALUES (%s, %s, %s, %s, %s);
        """
        
        # Ejecutar la consulta con la fecha de modificación
        cursor.execute(SQL_INSERT, (cliente_id, nombre, telefono, correo, fecha_modificacion))
        conn_postgres.commit()

        # Mensaje de éxito
        messagebox.showinfo("Éxito", f"Cliente '{nombre}' agregado correctamente.")

        # Limpiar los campos de entrada
        id_entry.delete(0, tk.END)
        nombre_entry.delete(0, tk.END)
        telefono_entry.delete(0, tk.END)
        core_entry.delete(0, tk.END)

    except Exception as e:
        # Mensaje de error
        messagebox.showerror("Error", f"No se pudo agregar el cliente. Detalles: {e}")
        conn_postgres.rollback()  # Revertir cambios si hay un error


def agregar_clientepostgre(ruut, conn_postgres):
    """
    Interfaz para agregar datos a la tabla 'Cliente'.
    """
    # Limpiar la ventana principal
    for widget in ruut.winfo_children():
        widget.destroy()

    # Crear un marco para el formulario
    frame = tk.Frame(ruut)
    frame.pack(pady=20)
    frame["bg"] = "#D4AF37"

    # Etiquetas y campos de entrada
    tk.Label(frame, text="Cliente ID", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    id_entry = tk.Entry(frame, font=("Arial", 12))
    id_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame, text="Nombre Cliente", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
    nombre_entry = tk.Entry(frame, font=("Arial", 12))
    nombre_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(frame, text="Número Telefónico", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5)
    telefono_entry = tk.Entry(frame, font=("Arial", 12))
    telefono_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(frame, text="Correo Electrónico", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5)
    core_entry = tk.Entry(frame, font=("Arial", 12))
    core_entry.grid(row=3, column=1, padx=10, pady=5)

    # Botón para agregar el cliente
    agregar_btn = tk.Button(
        frame,
        text="Agregar Cliente",
        font=("Arial", 12),
        command=lambda: insertar_cliente(conn_postgres, id_entry, nombre_entry, telefono_entry, core_entry)
    )
    agregar_btn.grid(row=4, column=0, columnspan=2, pady=10)

    # Botón para salir
    salir_btn = tk.Button(frame, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexionpostgre(ruut, conn_postgres))
    salir_btn.grid(row=5, column=0, columnspan=2, pady=10)



def actualizar_cliente_postgres(conn_postgres, cliente_id, nuevo_telefono, nuevo_correo, id_entry, telefono_entry, correo_entry):
    """
    Lógica para actualizar los datos del cliente (Teléfono y Correo), incluyendo la actualización de la fecha de modificación.
    """
    if not cliente_id:
        messagebox.showerror("Error", "El ID del cliente es obligatorio.")
        return

    try:
        # Construcción dinámica de la consulta
        parametros = []
        valores = []

        if nuevo_telefono:
            parametros.append('"Telefono" = %s')
            valores.append(nuevo_telefono)

        if nuevo_correo:
            parametros.append('"Correo" = %s')
            valores.append(nuevo_correo)

        # Agregar la actualización de la fecha de modificación
        parametros.append('"fecha_de_modificacion" = CURRENT_TIMESTAMP')
        
        # Verificar que se ha seleccionado al menos un campo para actualizar
        if not parametros:
            messagebox.showerror("Error", "Debe ingresar al menos un campo para actualizar.")
            return

        # Construye la consulta SQL dinámicamente
        set_clause = ", ".join(parametros)
        SQL_UPDATE = f"""UPDATE public.cliente
                          SET {set_clause}
                          WHERE "Cliente_ID" = %s"""
        valores.append(cliente_id)

        # Ejecuta la consulta
        cursor = conn_postgres.cursor()
        cursor.execute(SQL_UPDATE, tuple(valores))
        conn_postgres.commit()

        if cursor.rowcount == 0:
            messagebox.showwarning("Advertencia", f"No se encontró el cliente con ID '{cliente_id}'.")
        else:
            messagebox.showinfo("Éxito", f"Cliente con ID '{cliente_id}' actualizado correctamente.")

        # Limpiar los campos de entrada
        id_entry.delete(0, tk.END)
        telefono_entry.delete(0, tk.END)
        correo_entry.delete(0, tk.END)

        cursor.close()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar el cliente. Detalles: {e}")



def modificar_clientepostgre(ruut, conn_postgres):
    """
    Interfaz para modificar los datos de la tabla 'Cliente' (Teléfono y Correo).
    """
    # Limpiar la ventana principal
    for widget in ruut.winfo_children():
        widget.destroy()

    # Crear un marco para el formulario
    frame = tk.Frame(ruut)
    frame.pack(pady=20)
    frame["bg"] = "#87CEEB"

    # Etiquetas y campos de entrada
    tk.Label(frame, text="Cliente ID (a modificar)", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    id_entry = tk.Entry(frame, font=("Arial", 12))
    id_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame, text="Nuevo Teléfono (opcional)", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
    telefono_entry = tk.Entry(frame, font=("Arial", 12))
    telefono_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(frame, text="Nuevo Correo (opcional)", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5)
    correo_entry = tk.Entry(frame, font=("Arial", 12))
    correo_entry.grid(row=2, column=1, padx=10, pady=5)

    # Botón para actualizar los datos
    actualizar_btn = tk.Button(frame, text="Actualizar Cliente", font=("Arial", 12), 
                               command=lambda: actualizar_cliente_postgres(
                                   conn_postgres, 
                                   id_entry.get().strip(), 
                                   telefono_entry.get().strip(), 
                                   correo_entry.get().strip(),
                                   id_entry, 
                                   telefono_entry, 
                                   correo_entry
                               ))
    actualizar_btn.grid(row=3, column=0, columnspan=2, pady=10)

    # Botón para volver al menú anterior
    volver_btn = tk.Button(frame, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexionpostgre(ruut, conn_postgres))
    volver_btn.grid(row=4, column=0, columnspan=2, pady=10)



def eliminar_cliente_postgres(conn_postgres, cliente_id, id_entry):
    """
    Lógica para eliminar un cliente en la base de datos.
    """
    if not cliente_id:
        messagebox.showerror("Error", "El ID del cliente es obligatorio.")
        return

    try:
        # Ejecutar la eliminación en la base de datos
        cursor = conn_postgres.cursor()
        SQL_DELETE = """DELETE FROM public.cliente WHERE "Cliente_ID" = %s;"""
        cursor.execute(SQL_DELETE, (cliente_id,))
        conn_postgres.commit()

        if cursor.rowcount == 0:
            messagebox.showwarning("Advertencia", f"No se encontró el cliente con ID '{cliente_id}'.")
        else:
            messagebox.showinfo("Éxito", f"Cliente con ID '{cliente_id}' eliminado correctamente.")

        # Limpiar el campo de entrada
        id_entry.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar el cliente. Detalles: {e}")
    finally:
        cursor.close()


def borrar_clientepostgre(ruut, conn_postgres):
    """
    Interfaz para eliminar todos los registros de un cliente en específico usando su ID.
    """
    # Limpiar la ventana principal
    for widget in ruut.winfo_children():
        widget.destroy()

    # Crear un marco para el formulario
    frame = tk.Frame(ruut)
    frame.pack(pady=20)
    frame["bg"] = "#FF6347"

    # Etiquetas y campos de entrada
    tk.Label(frame, text="Cliente ID (a eliminar)", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    id_entry = tk.Entry(frame, font=("Arial", 12))
    id_entry.grid(row=0, column=1, padx=10, pady=5)

    # Botón para eliminar cliente
    eliminar_btn = tk.Button(frame, text="Eliminar Cliente", font=("Arial", 12), 
                             command=lambda: eliminar_cliente_postgres(
                                 conn_postgres, 
                                 id_entry.get().strip(), 
                                 id_entry
                             ))
    eliminar_btn.grid(row=1, column=0, columnspan=2, pady=10)

    # Botón para volver al menú anterior
    volver_btn = tk.Button(frame, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexionpostgre(ruut, conn_postgres))
    volver_btn.grid(row=2, column=0, columnspan=2, pady=10)