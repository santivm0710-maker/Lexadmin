from backend.database.connection import DatabaseConnection
from backend.entities import BitacoraEvento


class BitacoraService:
    """La bitácora es solo de lectura: se llena automáticamente desde
    `services.auditoria` cuando ocurren acciones en el sistema."""

    def listar(self):
        filas = DatabaseConnection.fetch_all(
            "SELECT * FROM bitacora ORDER BY id_bitacora DESC"
        )
        return [BitacoraEvento(**fila) for fila in filas]
