import psycopg2


class DatabaseManager:
    """
    Clase para manejar la conexión a la base de datos PostgreSQL.
    """

    def __init__(self, database, user, password, host, port):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None

    def connect(self):
        """
        Conectar a la base de datos.
        """
        try:
            self.connection = psycopg2.connect(
                database=self.database,
                user=self.user,
                host=self.host,
                password=self.password,
                port=self.port
            )
            print("Conexion exitosa a Postgres")
            return self.connection
        except Exception as e:
            print(f"Error al conectar con la base de datos: {e}")
            return None
