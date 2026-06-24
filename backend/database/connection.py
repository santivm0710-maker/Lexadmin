"""Prototipo de conexión a base de datos.

IMPORTANTE:
Este archivo NO abre una conexión real.
Solo deja preparada la estructura para una conexión futura.
"""

from dataclasses import dataclass

from backend.config import settings


@dataclass
class DatabaseConnectionPrototype:
    driver: str
    host: str
    port: int
    database: str
    user: str

    def get_connection_string_preview(self) -> str:
        """Retorna una cadena simulada sin mostrar la contraseña."""
        return f"{self.driver}://{self.user}:***@{self.host}:{self.port}/{self.database}"

    def connect(self):
        """Método reservado para conexión futura.

        En esta versión prototipo no se realiza conexión real.
        """
        raise NotImplementedError("La conexión real a base de datos todavía no está implementada.")


def get_database_prototype() -> DatabaseConnectionPrototype:
    return DatabaseConnectionPrototype(
        driver=settings.database_driver,
        host=settings.database_host,
        port=settings.database_port,
        database=settings.database_name,
        user=settings.database_user,
    )
