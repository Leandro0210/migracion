import pyodbc
import psycopg2


SERVER = 'Leandro'
DATABASE = 'Drinkers'
connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;'


try:
    # Conectar a SQL Server
    conn_sqlserver = pyodbc.connect(connectionString)
    print("Conexión exitosa a SQL Server")
    cursor_sqlserver = conn_sqlserver.cursor()


except pyodbc.Error as e:
    print(f"Error al conectar o ejecutar consulta en SQL Server: {e}")
    exit()

try:
    # Conectar a PostgreSQL
    conn_postgres = psycopg2.connect(database="Drinkers", user="postgres", host="localhost", password="HalaMadrid", port="5432")
    cursor_postgres = conn_postgres.cursor()
    print("Conexión exitosa a PostgreSQL")

    def run_tests(sql_server_conn, postgres_conn, queries):
        for i, query in enumerate(queries):
            print(f"\nPrueba {i+1}: Ejecutando consulta...")

            # Ejecutar el query en SQL Server
            sql_server_cursor = sql_server_conn.cursor()
            sql_server_cursor.execute(query)
            sql_server_data = sql_server_cursor.fetchall()

            # Ejecutar el query en PostgreSQL
            postgres_cursor = postgres_conn.cursor()
            postgres_cursor.execute(query)
            postgres_data = postgres_cursor.fetchall()

            # Limpiar los datos eliminando espacios innecesarios
            sql_server_data_cleaned = [tuple(map(lambda x: x.strip() if isinstance(x, str) else x, row)) for row in sql_server_data]
            postgres_data_cleaned = [tuple(map(lambda x: x.strip() if isinstance(x, str) else x, row)) for row in postgres_data]

            # Comparar resultados
            if sorted(sql_server_data_cleaned) == sorted(postgres_data_cleaned):
                print(f"Prueba {i+1}: Los resultados son iguales.")
            else:
                print(f"Prueba {i+1}: Los resultados son diferentes.")
                

    # Consultas para las pruebas
    queries = [
        """SELECT "Nombre_Emp" FROM empleado;""",
        """SELECT "Precio_Unitario" FROM Producto WHERE "Precio_Unitario" > 500;""",
        """Select "Nombre_Cat" from categoria;"""
    ]

    # Llamada a la función de pruebas
    run_tests(conn_sqlserver, conn_postgres, queries)

except psycopg2.Error as e:
    print(f"Error al conectar o ejecutar consulta en PostgreSQL: {e}")
    exit()

finally:
    # Cerrar conexiones
    if conn_sqlserver:
        conn_sqlserver.close()
    if conn_postgres:
        conn_postgres.close()
    print("Conexiones cerradas.")
