from backend.entities import Expediente
from backend.repositories.base_repository import BaseRepository


class ExpedienteRepository(BaseRepository[Expediente]):
    table_name = "expedientes"
    entity_class = Expediente
    pk_field = "id_expediente"
