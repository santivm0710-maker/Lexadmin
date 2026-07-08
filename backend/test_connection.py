from database.connection import DatabaseConnection

if __name__ == "__main__":
    if DatabaseConnection.test_connection():
        print(" La conexión funciona correctamente.")
    else:
        print(" Error al conectar.")