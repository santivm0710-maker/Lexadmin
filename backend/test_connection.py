"""Prueba rápida de conexión a MySQL.

Ejecutar desde la raíz del proyecto:
    python -m backend.test_connection
"""

from backend.database.connection import DatabaseConnection

if __name__ == "__main__":
    if DatabaseConnection.test_connection():
        print("La conexión funciona correctamente.")
    else:
        print("Error al conectar.")
