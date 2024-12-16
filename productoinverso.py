import pyodbc

SERVER = 'Leandro'  
DATABASE = 'Drinkers'
connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;'

def reversa(s):
    if len(s) == 0: 
        return ""
    return s[-1] + reversa(s[:-1])  

try:
    conn = pyodbc.connect(connectionString)
    print("Conexión exitosa")

    cursor = conn.cursor()
    sql_query = "SELECT Nombre_Pro FROM Producto"
    cursor.execute(sql_query)

    rows = cursor.fetchall()
    
    for row in rows:
        original_producto = row[0]
        producto_virado = reversa(original_producto)  
       
        cursor.execute("UPDATE Producto SET Producto_inverso = ? WHERE Nombre_Pro = ?", (producto_virado.strip(), original_producto))

    conn.commit()  
except pyodbc.Error as e:
    print(f"Error al conectar o ejecutar la consulta: {e}")
finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
    print("Conexión cerrada")
