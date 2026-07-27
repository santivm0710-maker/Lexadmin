from backend.entities import BitacoraEvento
from backend.repositories.base_repository import BaseRepository


class BitacoraRepository(BaseRepository[BitacoraEvento]):
    table_name = "bitacora"
    entity_class = BitacoraEvento
    pk_field = "id_evento"
