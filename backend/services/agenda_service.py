from backend.entities import EventoAgenda
from backend.repositories.agenda_repository import AgendaRepository
from backend.schemas.requests import AgendaCreate
from backend.services import auditoria

MODULO = "Agenda"


class AgendaService:
    def __init__(self):
        self.repository = AgendaRepository()

    def listar(self):
        return self.repository.list_all()

    def crear(self, datos: AgendaCreate) -> EventoAgenda:
        evento = self.repository.add(EventoAgenda(**datos.model_dump()))
        auditoria.registrar(MODULO, "Creación", f"Se programó: {evento.actividad} ({evento.fecha}).")
        return evento

    def actualizar(self, id_agenda: int, datos: AgendaCreate) -> "EventoAgenda | None":
        evento = self.repository.update(id_agenda, EventoAgenda(id_agenda=id_agenda, **datos.model_dump()))
        if evento is not None:
            auditoria.registrar(MODULO, "Actualización", f"Se actualizó el evento: {evento.actividad}.")
        return evento

    def eliminar(self, id_agenda: int) -> bool:
        eliminado = self.repository.delete(id_agenda)
        if eliminado:
            auditoria.registrar(MODULO, "Eliminación", f"Se eliminó el evento de agenda con ID {id_agenda}.")
        return eliminado
