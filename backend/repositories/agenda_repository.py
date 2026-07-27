from backend.entities import EventoAgenda
from backend.repositories.base_repository import BaseRepository


class AgendaRepository(BaseRepository[EventoAgenda]):
    table_name = "agenda"
    entity_class = EventoAgenda
    pk_field = "id_agenda"
