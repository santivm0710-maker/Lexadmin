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
