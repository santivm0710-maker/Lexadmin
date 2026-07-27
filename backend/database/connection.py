import mysql.connector
from mysql.connector import pooling

from backend.config import settings


class DatabaseConnection:

    _pool = None

    @classmethod
    def _get_pool(cls):
        if cls._pool is None:
            cls._pool = pooling.MySQLConnectionPool(
                pool_name="lexadmin_pool",
                pool_size=5,
                host=settings.database_host,
                port=settings.database_port,
                user=settings.database_user,
                password=settings.database_password,
                database=settings.database_name,
            )
        return cls._pool

    @classmethod
    def connect(cls):
        """
        Devuelve una conexión desde el pool.
        """
        return cls._get_pool().get_connection()

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

    @staticmethod
    def get_connection_string_preview():
        return (
            f"{settings.database_driver}://{settings.database_user}:***@"
            f"{settings.database_host}:{settings.database_port}/{settings.database_name}"
        )


def get_database_prototype():
    return DatabaseConnection()