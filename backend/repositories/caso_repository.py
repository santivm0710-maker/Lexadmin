from backend.entities import Caso
from backend.repositories.base_repository import BaseRepository


class CasoRepository(BaseRepository[Caso]):
    table_name = "casos"
    entity_class = Caso
    pk_field = "id_caso"
