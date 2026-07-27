"""Conexión a MySQL y utilidades de consulta.

Toda la aplicación accede a la base de datos a través de esta capa,
que mantiene un pool de conexiones y ofrece helpers cómodos para
ejecutar consultas sin repetir el manejo de cursores.
"""

import mysql.connector
from mysql.connector import pooling

from backend.config import settings


class DatabaseConnection:

    _pool = None

    @classmethod
    def _get_pool(cls):
        # El pool se crea la primera vez que se necesita, no al importar,
        # para que el backend arranque aunque MySQL aún no esté disponible.
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
        """Devuelve una conexión tomada del pool."""
        return cls._get_pool().get_connection()

    @staticmethod
    def close(connection):
        if connection and connection.is_connected():
            connection.close()

    # ------------------------------------------------------------------
    # Helpers de consulta
    # ------------------------------------------------------------------
    @classmethod
    def fetch_all(cls, sql, params=None):
        """Devuelve todas las filas de una consulta como lista de dicts."""
        connection = cls.connect()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, params or ())
            filas = cursor.fetchall()
            cursor.close()
            return filas
        finally:
            cls.close(connection)

    @classmethod
    def fetch_one(cls, sql, params=None):
        """Devuelve la primera fila como dict, o None si no hay resultados."""
        connection = cls.connect()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, params or ())
            fila = cursor.fetchone()
            cursor.close()
            return fila
        finally:
            cls.close(connection)

    @classmethod
    def execute(cls, sql, params=None):
        """Ejecuta INSERT/UPDATE/DELETE y devuelve (id_generado, filas_afectadas)."""
        connection = cls.connect()
        try:
            cursor = connection.cursor()
            cursor.execute(sql, params or ())
            connection.commit()
            resultado = (cursor.lastrowid, cursor.rowcount)
            cursor.close()
            return resultado
        finally:
            cls.close(connection)

    @staticmethod
    def test_connection():
        try:
            DatabaseConnection.fetch_one("SELECT 1")
            print("Conexión exitosa con MySQL.")
            return True
        except mysql.connector.Error as e:
            print(f"Error de conexión: {e}")
            return False

    @staticmethod
    def get_connection_string_preview():
        return (
            f"{settings.database_driver}://{settings.database_user}:***@"
            f"{settings.database_host}:{settings.database_port}/{settings.database_name}"
        )


def get_database_prototype():
    return DatabaseConnection()
