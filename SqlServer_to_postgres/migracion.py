import pyodbc
import psycopg2
from cerrar.interfaz_postgre import interfaz
from datetime import datetime
from clase.conexion import *
# Configuración de SQL Server
SERVER = 'Leandro'
DATABASE = 'Drinkers'
connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;'

# Mapeo de tipos de datos de SQL Server a PostgreSQL
tipo_mapeo = {
    'nvarchar': 'TEXT',
    'int': 'INTEGER',
    'datetime': 'TIMESTAMP'
}

try:
    # Conectar a SQL Server
    conn_sqlserver = pyodbc.connect(connectionString)
    print("Conexión exitosa a SQL Server")
    cursor_sqlserver = conn_sqlserver.cursor()

    # Obtener todas las tablas de SQL Server
    cursor_sqlserver.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
    tablas_sqlserver = [fila[0] for fila in cursor_sqlserver.fetchall()]

except pyodbc.Error as e:
    print(f"Error al conectar o ejecutar consulta en SQL Server: {e}")
    exit()

try:
    # Conectar a PostgreSQL
    db_manager = DatabaseManager(database="Drinkers", user="postgres", host="localhost", password="HalaMadrid",  port="5432")
    conn_postgres = db_manager.connect()
    cursor_postgres = conn_postgres.cursor()

    # Iterar sobre cada tabla de SQL Server
    for tabla in tablas_sqlserver:
        # Obtener estructura de la tabla actual
        cursor_sqlserver.execute(f"""
        SELECT COLUMN_NAME, DATA_TYPE 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = '{tabla}'
        """)
        columnas_info = cursor_sqlserver.fetchall()
        columnas = [col[0] for col in columnas_info]
        
        # Definir columnas y sus tipos para PostgreSQL
        columnas_definicion = []
        for columna, tipo in columnas_info:
            tipo_postgres = tipo_mapeo.get(tipo, 'TEXT')  # Predeterminado: TEXT
            columnas_definicion.append(f'"{columna}" {tipo_postgres}')
        columnas_definicion.append('"fecha_de_modificacion" TIMESTAMP')
        columnas_definicion_str = ", ".join(columnas_definicion)

        # Crear la tabla en PostgreSQL si no existe
        primary_key = columnas[0]  # Asumimos que la primera columna es la clave primaria
        cursor_postgres.execute(f"""
        CREATE TABLE IF NOT EXISTS "{tabla.lower()}" (
            {columnas_definicion_str},
            PRIMARY KEY ("{primary_key}")
        );
        """)
        conn_postgres.commit()

        # Obtener datos de la tabla actual
        cursor_sqlserver.execute(f"SELECT * FROM {tabla}")
        data_sqlserver = cursor_sqlserver.fetchall()

        # Insertar o actualizar datos en PostgreSQL
        insert_query = f"""
        INSERT INTO "{tabla.lower()}" ({', '.join([f'"{col}"' for col in columnas])}, "fecha_de_modificacion")
        VALUES ({', '.join(['%s'] * len(columnas))}, CURRENT_TIMESTAMP)
        ON CONFLICT ("{primary_key}")
        DO UPDATE SET 
            {', '.join([f'"{col}" = EXCLUDED."{col}"' for col in columnas[1:]])},
            "fecha_de_modificacion" = CASE
                WHEN ({' OR '.join([f"EXCLUDED.\"{col}\" <> \"{tabla.lower()}\".\"{col}\"" for col in columnas[1:]])})
                THEN CURRENT_TIMESTAMP
                ELSE "{tabla.lower()}".fecha_de_modificacion
            END;
        """
        cursor_postgres.executemany(insert_query, data_sqlserver)
        conn_postgres.commit()
        print(f"Datos de la tabla {tabla} migrados correctamente")

except psycopg2.Error as e:
    print(f"Error al conectar o ejecutar consulta en PostgreSQL: {e}")
    exit()

finally:
    # Cerrar conexiones
    cursor_sqlserver.close()
    conn_sqlserver.close()
    cursor_postgres.close()
    conn_postgres.close()
    print("Conexiones cerradas")
    interfaz()
