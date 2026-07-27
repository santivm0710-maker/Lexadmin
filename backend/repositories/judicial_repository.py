from backend.entities import InformacionJudicial
from backend.repositories.base_repository import BaseRepository


class JudicialRepository(BaseRepository[InformacionJudicial]):
    table_name = "informacion_judicial"
    entity_class = InformacionJudicial
    pk_field = "id_info_judicial"
