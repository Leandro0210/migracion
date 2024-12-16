import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import psycopg2
from datetime import datetime
from cerrarpo.closepostg import cerrar_conexionpostgre

def producto_postgre(ruut, conn_postgres):
   
    try:
        # Consulta SQL para obtener los registros de la tabla 'categoria'
        SQL_QUERY = """
        SELECT *FROM producto
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

def insertar_producto(conn_postgres, id_entry, subcategoria_entry, nombre_entry, contenido_entry, precio_entry, stock_entry):
    """
    Inserta un producto en la base de datos PostgreSQL.
    """
    # Obtener valores de los campos de entrada
    producto_id = id_entry.get().strip()
    subcategoria_id = subcategoria_entry.get().strip()
    nombre_pro = nombre_entry.get().strip()
    contenido = contenido_entry.get().strip()
    precio_unitario = precio_entry.get().strip()
    stock = stock_entry.get().strip()

    # Validar que no haya campos vacíos
    if not producto_id or not subcategoria_id or not nombre_pro or not contenido or not precio_unitario or not stock:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    try:
        # Insertar datos en la base de datos PostgreSQL
        cursor = conn_postgres.cursor()
        fecha_modificacion = datetime.now()
        SQL_INSERT = """
       INSERT INTO public.producto(
	 "Producto_ID", "Subcategoria_ID", "Nombre_Pro", "Contenido", "Precio_Unitario", "Stock", fecha_de_modificacion)
	 VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(SQL_INSERT, (producto_id, subcategoria_id, nombre_pro, contenido, precio_unitario, stock, fecha_modificacion))
        conn_postgres.commit()

        # Mensaje de éxito
        messagebox.showinfo("Éxito", f"Producto '{nombre_pro}' agregado correctamente.")

        # Limpiar los campos de entrada
        id_entry.delete(0, tk.END)
        subcategoria_entry.delete(0, tk.END)
        nombre_entry.delete(0, tk.END)
        contenido_entry.delete(0, tk.END)
        precio_entry.delete(0, tk.END)
        stock_entry.delete(0, tk.END)

    except Exception as e:
        # Mensaje de error
        conn_postgres.rollback()
        messagebox.showerror("Error", f"No se pudo agregar el producto. Detalles: {e}")


def agregar_productopostgre(ruut, conn_postgres):
    """
    Interfaz para agregar datos a la tabla 'Producto' en PostgreSQL.
    """
    # Limpiar la ventana principal
    for widget in ruut.winfo_children():
        widget.destroy()

    # Crear un marco para el formulario
    frame = tk.Frame(ruut)
    frame.pack(pady=20)
    frame["bg"] = "#D4AF37"

    # Etiquetas y campos de entrada
    tk.Label(frame, text="Producto ID", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    id_entry = tk.Entry(frame, font=("Arial", 12))
    id_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame, text="Subcategoria ID", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
    subcategoria_entry = tk.Entry(frame, font=("Arial", 12))
    subcategoria_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(frame, text="Nombre Producto", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5)
    nombre_entry = tk.Entry(frame, font=("Arial", 12))
    nombre_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(frame, text="Contenido", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5)
    contenido_entry = tk.Entry(frame, font=("Arial", 12))
    contenido_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(frame, text="Precio Unitario", font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=5)
    precio_entry = tk.Entry(frame, font=("Arial", 12))
    precio_entry.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(frame, text="Stock", font=("Arial", 12)).grid(row=5, column=0, padx=10, pady=5)
    stock_entry = tk.Entry(frame, font=("Arial", 12))
    stock_entry.grid(row=5, column=1, padx=10, pady=5)

    # Botón para agregar el producto
    agregar_btn = tk.Button(
        frame,
        text="Agregar Producto",
        font=("Arial", 12),
        command=lambda: insertar_producto(conn_postgres, id_entry, subcategoria_entry, nombre_entry, contenido_entry, precio_entry, stock_entry)
    )
    agregar_btn.grid(row=6, column=0, columnspan=2, pady=10)

    # Botón para salir
    salir_btn = tk.Button(frame, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexionpostgre(ruut, conn_postgres))
    salir_btn.grid(row=7, column=0, columnspan=2, pady=10)


def borrar_productopostgre(ruut, conn_postgres):
    """
    Interfaz para eliminar todos los registros de un producto en específico usando su ID.
    """
    # Limpiar la ventana principal
    for widget in ruut.winfo_children():
        widget.destroy()

    # Crear un marco para el formulario
    frame = tk.Frame(ruut)
    frame.pack(pady=20)
    frame["bg"] = "#FF6347"

    # Etiquetas y campos de entrada
    tk.Label(frame, text="Producto ID (a eliminar)", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    id_entry = tk.Entry(frame, font=("Arial", 12))
    id_entry.grid(row=0, column=1, padx=10, pady=5)

    # Función para eliminar producto
    def eliminar_producto():
        producto_id = id_entry.get().strip()

        if not producto_id:
            messagebox.showerror("Error", "El ID del producto es obligatorio.")
            return

        try:
            # Ejecutar la eliminación en la base de datos
            cursor = conn_postgres.cursor()
            SQL_DELETE = """DELETE FROM public.producto WHERE "Producto_ID" = %s;"""
            cursor.execute(SQL_DELETE, (producto_id,))
            conn_postgres.commit()

            if cursor.rowcount == 0:
                messagebox.showwarning("Advertencia", f"No se encontró el producto con ID '{producto_id}'.")
            else:
                messagebox.showinfo("Éxito", f"Producto con ID '{producto_id}' eliminado correctamente.")

            # Limpiar el campo de entrada
            id_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el producto. Detalles: {e}")
        finally:
            cursor.close()

    # Botón para eliminar producto
    eliminar_btn = tk.Button(frame, text="Eliminar Producto", font=("Arial", 12), command=eliminar_producto)
    eliminar_btn.grid(row=1, column=0, columnspan=2, pady=10)

    # Botón para volver al menú anterior
    volver_btn = tk.Button(frame, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexionpostgre(ruut, conn_postgres))
    volver_btn.grid(row=2, column=0, columnspan=2, pady=10)


def modificar_productopostgre(ruut, conn_postgre):
    """
    Interfaz para modificar los datos de la tabla 'Producto' en PostgreSQL.
    El usuario puede actualizar solo la cantidad, solo el precio, o ambos.
    """
    # Limpiar la ventana principal
    for widget in ruut.winfo_children():
        widget.destroy()

    # Crear un marco para el formulario
    frame = tk.Frame(ruut)
    frame.pack(pady=20)
    frame["bg"] = "#87CEEB"

    # Etiquetas y campos de entrada
    tk.Label(frame, text="Producto ID (a modificar)", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    id_entry = tk.Entry(frame, font=("Arial", 12))
    id_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame, text="Nuevo Stock (Opcional)", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
    cantidad_entry = tk.Entry(frame, font=("Arial", 12))
    cantidad_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(frame, text="Nuevo Precio (Opcional)", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5)
    precio_entry = tk.Entry(frame, font=("Arial", 12))
    precio_entry.grid(row=2, column=1, padx=10, pady=5)

    # Función para modificar datos
    def actualizar_producto():
        producto_id = id_entry.get().strip()
        nueva_cantidad = cantidad_entry.get().strip()
        nuevo_precio = precio_entry.get().strip()

        if not producto_id:
            messagebox.showerror("Error", "El campo 'Producto ID' es obligatorio.")
            return

        try:
            # Construir la consulta SQL dinámicamente
            cursor = conn_postgre.cursor()
            campos_a_actualizar = []
            valores = []

            # Validar si el campo cantidad fue llenado
            if nueva_cantidad:
                campos_a_actualizar.append('"Stock" = %s')
                valores.append(nueva_cantidad)

            # Validar si el campo precio fue llenado
            if nuevo_precio:
                campos_a_actualizar.append('"Precio_Unitario" = %s')
                valores.append(nuevo_precio)

            # Si no hay nada para actualizar
            if not campos_a_actualizar:
                messagebox.showerror("Error", "Debe ingresar al menos un campo para actualizar (cantidad o precio).")
                return

            # Agregar la fecha de modificación
            campos_a_actualizar.append('"fecha_de_modificacion" = NOW()')

            # Construir la consulta SQL
            sql = f"""UPDATE public.producto
                      SET {', '.join(campos_a_actualizar)}
                      WHERE "Producto_ID" = %s;"""
            valores.append(producto_id)

            # Ejecutar la consulta
            cursor.execute(sql, tuple(valores))
            conn_postgre.commit()

            if cursor.rowcount == 0:
                messagebox.showwarning("Advertencia", f"No se encontró el producto con ID '{producto_id}'.")
            else:
                messagebox.showinfo("Éxito", f"Producto con ID '{producto_id}' actualizado correctamente.")

            # Limpiar los campos de entrada
            id_entry.delete(0, tk.END)
            cantidad_entry.delete(0, tk.END)
            precio_entry.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el producto. Detalles: {e}")
        finally:
            cursor.close()

    # Botón para actualizar los datos
    actualizar_btn = tk.Button(frame, text="Actualizar Producto", font=("Arial", 12), command=actualizar_producto)
    actualizar_btn.grid(row=3, column=0, columnspan=2, pady=10)

    # Botón para volver al menú anterior
    volver_btn = tk.Button(frame, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexionpostgre(ruut, conn_postgre))
    volver_btn.grid(row=4, column=0, columnspan=2, pady=10)
