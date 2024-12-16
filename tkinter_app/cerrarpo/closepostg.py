def cerrar_conexionpostgre(ruut, conn_postgres):
    try:
        # Cerrar la conexión de la base de datos
        conn_postgres.close()
        print("Conexión cerrada")
    except Exception as e:
        print(f"Error al cerrar la conexión: {e}")
    
    # Salir de la aplicación
    ruut.quit()  