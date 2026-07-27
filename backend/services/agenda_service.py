from backend.entities import EventoAgenda
from backend.repositories.agenda_repository import AgendaRepository
from backend.schemas.requests import AgendaCreate


class AgendaService:
    def __init__(self):
        self.repository = AgendaRepository()

    def listar(self):
        return self.repository.list_all()

    def crear(self, datos: AgendaCreate) -> EventoAgenda:
        return self.repository.add(EventoAgenda(id_evento=0, **datos.model_dump()))

    def actualizar(self, id_evento: int, datos: AgendaCreate) -> EventoAgenda | None:
        return self.repository.update(id_evento, EventoAgenda(id_evento=id_evento, **datos.model_dump()))

    def eliminar(self, id_evento: int) -> bool:
        return self.repository.delete(id_evento)
