from backend.database.connection import DatabaseConnection
from backend.entities import Usuario
from backend.repositories.base_repository import BaseRepository


class UsuarioRepository(BaseRepository[Usuario]):
    table_name = "usuarios"
    entity_class = Usuario
    pk_field = "id_usuario"

    def get_by_correo(self, correo: str) -> "Usuario | None":
        fila = DatabaseConnection.fetch_one(
            "SELECT * FROM usuarios WHERE correo = %s", (correo,)
        )
        return Usuario(**fila) if fila else None
