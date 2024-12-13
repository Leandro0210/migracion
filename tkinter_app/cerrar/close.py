def cerrar_conexion(root, conn):
    try:
        # Cerrar la conexión de la base de datos
        conn.close()
        print("Conexión cerrada")
    except Exception as e:
        print(f"Error al cerrar la conexión: {e}")
    
    # Salir de la aplicación
    root.quit()  
