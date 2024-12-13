import pyodbc
import tkinter as tk
from tkinter import ttk
from cerrar.close import cerrar_conexion
from tkinter import messagebox


def mues_pro(conn):
    """
    Muestra los registros de la tabla 'Producto' en una tabla gráfica (Treeview)
    usando la conexión proporcionada y la clase Product.
    """
    try:
        # Define la consulta SQL para recuperar los productos
        SQL_QUERY = "SELECT Producto_ID, Subcategoria_ID, Nombre_Pro, Contenido, Precio_Unitario, Stock FROM producto"  # Ajusta las columnas según tu tabla

        # Crear un cursor y ejecutar la consulta
        cursor = conn.cursor()
        cursor.execute(SQL_QUERY)

        # Crear ventana de Tkinter para mostrar los datos
        ventana = tk.Tk()
        ventana.title("Productos")
        ventana.geometry("800x400")
        ventana.iconbitmap("logo.ico")
        

        # Crear Treeview con las columnas necesarias
        tabla = ttk.Treeview(ventana, columns=("ID", "Subcategoria", "Nombre", "Contenido", "Precio", "Stock"), show="headings")
        tabla.pack(fill=tk.BOTH, expand=True)
        
        # Configurar encabezados del Treeview
        tabla.heading("ID", text="ID", anchor=tk.CENTER)
        tabla.heading("Subcategoria", text="Subcategoria", anchor=tk.CENTER)
        tabla.heading("Nombre", text="Nombre", anchor=tk.CENTER)
        tabla.heading("Contenido", text="Contenido", anchor=tk.CENTER)
        tabla.heading("Precio", text="Precio Unitario", anchor=tk.CENTER)
        tabla.heading("Stock", text="Stock", anchor=tk.CENTER)

        tabla.column("ID", anchor=tk.CENTER, width=100)
        tabla.column("Subcategoria", anchor=tk.CENTER, width=100)
        tabla.column("Nombre", anchor=tk.CENTER, width=200)
        tabla.column("Contenido", anchor=tk.CENTER, width=150)
        tabla.column("Precio", anchor=tk.CENTER, width=100)
        tabla.column("Stock", anchor=tk.CENTER, width=100)

        # Recuperar los registros y crear instancias de la clase Product
        rows = cursor.fetchall()
        for row in rows:
            # Crear una instancia de Product
            producto = Product(row[0], row[1], row[2], row[3], row[4], row[5])

            # Insertar los datos de la instancia Product en el Treeview
            tabla.insert("", tk.END, values=(producto.producto_id, producto.subcategoria_id, producto.nombre_pro, producto.contenido, producto.precio_unitario, producto.stock))

        # Cerrar el cursor
        cursor.close()

    except pyodbc.Error as e:
        print(f"Error al consultar la base de datos: {e}")


def insertar_producto(conn, id_entry, subcategoria_entry, nombre_entry, contenido_entry, precio_entry, stock_entry):
    """
    Inserta un producto en la base de datos.
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
        # Insertar datos en la base de datos
        cursor = conn.cursor()
        SQL_INSERT = """
        INSERT INTO producto (Producto_ID, Subcategoria_ID, Nombre_Pro, Contenido, Precio_Unitario, Stock)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor.execute(SQL_INSERT, (producto_id, subcategoria_id, nombre_pro, contenido, float(precio_unitario), int(stock)))
        conn.commit()

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
        messagebox.showerror("Error", f"No se pudo agregar el producto. Detalles: {e}")


def agre_pro(root, conn):
    """
    Interfaz para agregar datos a la tabla 'Producto'.
    """
    # Limpiar la ventana principal
    for widget in root.winfo_children():
        widget.destroy()

    # Crear un marco para el formulario
    frame = tk.Frame(root)
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
        command=lambda: insertar_producto(conn, id_entry, subcategoria_entry, nombre_entry, contenido_entry, precio_entry, stock_entry)
    )
    agregar_btn.grid(row=6, column=0, columnspan=2, pady=10)

    # Botón para salir
    salir_btn = tk.Button(frame, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexion(root, conn))
    salir_btn.grid(row=7, column=0, columnspan=2, pady=10)



def mod_pro(root, conn):
    """
    Interfaz para modificar el Precio_Unitario y Stock de la tabla 'Producto'.
    """
    # Limpiar la ventana principal
    for widget in root.winfo_children():
        widget.destroy()

    # Crear un marco para el formulario
    frame = tk.Frame(root)
    frame.pack(pady=20)
    frame["bg"] = "#87CEEB"

    # Etiquetas y campos de entrada
    tk.Label(frame, text="Producto ID (a modificar)", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    id_entry = tk.Entry(frame, font=("Arial", 12))
    id_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(frame, text="Nuevo Precio Unitario (opcional)", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
    precio_entry = tk.Entry(frame, font=("Arial", 12))
    precio_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(frame, text="Nuevo Stock (opcional)", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5)
    stock_entry = tk.Entry(frame, font=("Arial", 12))
    stock_entry.grid(row=2, column=1, padx=10, pady=5)

    # Función para modificar datos
    def actualizar_producto():
        producto_id = id_entry.get().strip()
        nuevo_precio = precio_entry.get().strip()
        nuevo_stock = stock_entry.get().strip()

        if not producto_id:
            messagebox.showerror("Error", "El ID del producto es obligatorio.")
            return
        
        try:
            # Inicializa una lista de parámetros para la consulta
            parametros = []

            # Verifica si el precio fue proporcionado
            if nuevo_precio:
                parametros.append(f"Precio_Unitario = {nuevo_precio}")
            
            # Verifica si el stock fue proporcionado
            if nuevo_stock:
                parametros.append(f"Stock = {nuevo_stock}")

            if not parametros:
                messagebox.showerror("Error", "Debe ingresar al menos un campo para actualizar.")
                return

            # Construye la consulta SQL
            set_clause = ", ".join(parametros)
            SQL_UPDATE = f"UPDATE Producto SET {set_clause} WHERE Producto_ID = ?"

            # Ejecuta la consulta
            cursor = conn.cursor()
            cursor.execute(SQL_UPDATE, (producto_id,))
            conn.commit()

            if cursor.rowcount == 0:
                messagebox.showwarning("Advertencia", f"No se encontró el producto con ID '{producto_id}'.")
            else:
                messagebox.showinfo("Éxito", f"Producto con ID '{producto_id}' actualizado correctamente.")
            
            # Limpiar los campos de entrada
            id_entry.delete(0, tk.END)
            precio_entry.delete(0, tk.END)
            stock_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el producto. Detalles: {e}")

    # Botón para actualizar los datos
    actualizar_btn = tk.Button(frame, text="Actualizar Producto", font=("Arial", 12), command=actualizar_producto)
    actualizar_btn.grid(row=3, column=0, columnspan=2, pady=10)

    # Botón para volver al menú anterior
    volver_btn = tk.Button(frame, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexion(root, conn))
    volver_btn.grid(row=4, column=0, columnspan=2, pady=10)


def del_pro(root, conn):
    """
    Interfaz para eliminar un registro de la tabla 'Producto' dado su Producto_ID.
    """
    # Limpiar la ventana principal
    for widget in root.winfo_children():
        widget.destroy()

    # Crear un marco para el formulario
    frame = tk.Frame(root)
    frame.pack(pady=20)
    frame["bg"] = "#98FB98"

    # Etiquetas y campos de entrada
    tk.Label(frame, text="Producto ID (a eliminar)", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    producto_id_entry = tk.Entry(frame, font=("Arial", 12))
    producto_id_entry.grid(row=0, column=1, padx=10, pady=5)

    # Función para eliminar un registro
    def eliminar_producto():
        producto_id = producto_id_entry.get().strip()

        if not producto_id:
            messagebox.showerror("Error", "El ID del producto es obligatorio.")
            return

        try:
            # Eliminar registro en la base de datos
            cursor = conn.cursor()
            SQL_DELETE = "DELETE FROM Producto WHERE Producto_ID = ?"
            cursor.execute(SQL_DELETE, (producto_id,))
            conn.commit()

            if cursor.rowcount == 0:
                messagebox.showwarning("Advertencia", f"No se encontró el producto con ID '{producto_id}'.")
            else:
                messagebox.showinfo("Éxito", f"Producto con ID '{producto_id}' eliminado correctamente.")

            # Limpiar el campo de entrada
            producto_id_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el producto. Detalles: {e}")

    # Botón para eliminar el registro
    eliminar_btn = tk.Button(frame, text="Eliminar Producto", font=("Arial", 12), command=eliminar_producto)
    eliminar_btn.grid(row=1, column=0, columnspan=2, pady=10)

    # Botón para volver al menú anterior
    volver_btn = tk.Button(frame, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexion(root, conn))
    volver_btn.grid(row=2, column=0, columnspan=2, pady=10)
