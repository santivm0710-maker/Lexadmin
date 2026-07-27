from backend.database.connection import DatabaseConnection
from backend.entities import BitacoraEvento
from backend.repositories.base_repository import BaseRepository


class BitacoraRepository(BaseRepository[BitacoraEvento]):
    table_name = "bitacora"
    entity_class = BitacoraEvento
    pk_field = "id_bitacora"

    def list_recent(self, limite=8):
        """Devuelve los eventos más recientes (para el dashboard)."""
        filas = DatabaseConnection.fetch_all(
            "SELECT * FROM bitacora ORDER BY id_bitacora DESC LIMIT %s", (limite,)
        )
        return [self.entity_class(**fila) for fila in filas]
