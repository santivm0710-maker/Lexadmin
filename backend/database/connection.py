import mysql.connector
from mysql.connector import pooling

from config import settings


class DatabaseConnection:

    _pool = pooling.MySQLConnectionPool(
        pool_name="lexadmin_pool",
        pool_size=5,
        host=settings.database_host,
        port=settings.database_port,
        user=settings.database_user,
        password=settings.database_password,
        database=settings.database_name,
    )

    @classmethod
    def connect(cls):
        """
        Devuelve una conexión desde el pool.
        """
        return cls._pool.get_connection()

    @staticmethod
    def close(connection):
        if connection and connection.is_connected():
            connection.close()

    @staticmethod
    def test_connection():
        connection = None

        try:
            connection = DatabaseConnection.connect()

            if connection.is_connected():
                print("Conexión exitosa con MySQL.")
                return True

        except mysql.connector.Error as e:
            print(f"Error de conexión: {e}")
            return False

        finally:
            if connection:
                connection.close()