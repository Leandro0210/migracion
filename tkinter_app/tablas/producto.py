import pyodbc
import tkinter as tk
from tkinter import ttk
from cerrar.close import cerrar_conexion
from tkinter import messagebox

def mostrar_productos(conn):
    """
    Muestra los registros de la tabla 'Producto' en una tabla gráfica (Treeview)
    
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

        # Recuperar los registros y insertarlos en el Treeview
        rows = cursor.fetchall()
        for row in rows:
            tabla.insert("", tk.END, values=(row[0], row[1], row[2], row[3], row[4], row[5]))

        # Cerrar el cursor
        cursor.close()

    except pyodbc.Error as e:
        print(f"Error al consultar la base de datos: {e}")


def insertar_producto(conn, id_entrada, subcategoria_entrada, nombre_entrada, contenido_entrada, precio_entrada, stock_entrada):
    """
    Inserta un producto en la base de datos.
    """
    # Obtener valores de los campos de entrada
    producto_id = id_entrada.get().strip()
    subcategoria_id = subcategoria_entrada.get().strip()
    nombre_pro = nombre_entrada.get().strip()
    contenido = contenido_entrada.get().strip()
    precio_unitario = precio_entrada.get().strip()
    stock = stock_entrada.get().strip()

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
        id_entrada.delete(0, tk.END)
        subcategoria_entrada.delete(0, tk.END)
        nombre_entrada.delete(0, tk.END)
        contenido_entrada.delete(0, tk.END)
        precio_entrada.delete(0, tk.END)
        stock_entrada.delete(0, tk.END)

    except Exception as e:
        # Mensaje de error
        messagebox.showerror("Error", f"No se pudo agregar el producto. Detalles: {e}")


def agregar_producto(root, conn):
    """
    Interfaz para agregar datos a la tabla 'Producto'.
    """
    # Limpiar la ventana principal
    for widget in root.winfo_children():
        widget.destroy()

    # Crear un marco para el formulario
    marco = tk.Frame(root)
    marco.pack(pady=20)
    marco["bg"] = "#D4AF37"

    # Etiquetas y campos de entrada
    tk.Label(marco, text="Producto ID", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    id_entrada = tk.Entry(marco, font=("Arial", 12))
    id_entrada.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(marco, text="Subcategoria ID", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
    subcategoria_entrada = tk.Entry(marco, font=("Arial", 12))
    subcategoria_entrada.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(marco, text="Nombre Producto", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5)
    nombre_entrada = tk.Entry(marco, font=("Arial", 12))
    nombre_entrada.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(marco, text="Contenido", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5)
    contenido_entrada = tk.Entry(marco, font=("Arial", 12))
    contenido_entrada.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(marco, text="Precio Unitario", font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=5)
    precio_entrada = tk.Entry(marco, font=("Arial", 12))
    precio_entrada.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(marco, text="Stock", font=("Arial", 12)).grid(row=5, column=0, padx=10, pady=5)
    stock_entrada = tk.Entry(marco, font=("Arial", 12))
    stock_entrada.grid(row=5, column=1, padx=10, pady=5)

    # Botón para agregar el producto
    agregar_boton = tk.Button(
        marco,
        text="Agregar Producto",
        font=("Arial", 12),
        command=lambda: insertar_producto(conn, id_entrada, subcategoria_entrada, nombre_entrada, contenido_entrada, precio_entrada, stock_entrada)
    )
    agregar_boton.grid(row=6, column=0, columnspan=2, pady=10)

    # Botón para salir
    salir_boton = tk.Button(marco, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexion(root, conn))
    salir_boton.grid(row=7, column=0, columnspan=2, pady=10)



def actualizar_producto(root, conn, id_entrada, precio_entrada, stock_entrada):
    """
    Función para modificar los datos de un producto.
    """
    producto_id = id_entrada.get().strip()
    nuevo_precio = precio_entrada.get().strip()
    nuevo_stock = stock_entrada.get().strip()

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
        id_entrada.delete(0, tk.END)
        precio_entrada.delete(0, tk.END)
        stock_entrada.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar el producto. Detalles: {e}")

def modificar_producto(root, conn):
    """
    Interfaz para modificar el Precio_Unitario y Stock de la tabla 'Producto'.
    """
    # Limpiar la ventana principal
    for widget in root.winfo_children():
        widget.destroy()

    # Crear un marco para el formulario
    marco = tk.Frame(root)
    marco.pack(pady=20)
    marco["bg"] = "#87CEEB"

    # Etiquetas y campos de entrada
    tk.Label(marco, text="Producto ID (a modificar)", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    id_entrada = tk.Entry(marco, font=("Arial", 12))
    id_entrada.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(marco, text="Nuevo Precio Unitario (opcional)", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
    precio_entrada = tk.Entry(marco, font=("Arial", 12))
    precio_entrada.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(marco, text="Nuevo Stock (opcional)", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5)
    stock_entrada = tk.Entry(marco, font=("Arial", 12))
    stock_entrada.grid(row=2, column=1, padx=10, pady=5)

    # Botón para actualizar los datos
    actualizar_boton = tk.Button(marco, text="Actualizar Producto", font=("Arial", 12), 
                                 command=lambda: actualizar_producto(root, conn, id_entrada, precio_entrada, stock_entrada))
    actualizar_boton.grid(row=3, column=0, columnspan=2, pady=10)

    # Botón para volver al menú anterior
    volver_boton = tk.Button(marco, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexion(root, conn))
    volver_boton.grid(row=4, column=0, columnspan=2, pady=10)


def eliminar_producto(root, conn, producto_id_entrada):
    """
    Función para eliminar un producto de la base de datos dado su Producto_ID.
    """
    producto_id = producto_id_entrada.get().strip()

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
        producto_id_entrada.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar el producto. Detalles: {e}")

def borrar_producto(root, conn):
    """
    Interfaz para eliminar un registro de la tabla 'Producto' dado su Producto_ID.
    """
    # Limpiar la ventana principal
    for widget in root.winfo_children():
        widget.destroy()

    # Crear un marco para el formulario
    marco = tk.Frame(root)
    marco.pack(pady=20)
    marco["bg"] = "#98FB98"

    # Etiquetas y campos de entrada
    tk.Label(marco, text="Producto ID (a eliminar)", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
    producto_id_entrada = tk.Entry(marco, font=("Arial", 12))
    producto_id_entrada.grid(row=0, column=1, padx=10, pady=5)

    # Botón para eliminar el registro
    eliminar_boton = tk.Button(marco, text="Eliminar Producto", font=("Arial", 12), 
                               command=lambda: eliminar_producto(root, conn, producto_id_entrada))
    eliminar_boton.grid(row=1, column=0, columnspan=2, pady=10)

    # Botón para volver al menú anterior
    volver_boton = tk.Button(marco, text="Salir", font=("Arial", 12), command=lambda: cerrar_conexion(root, conn))
    volver_boton.grid(row=2, column=0, columnspan=2, pady=10)