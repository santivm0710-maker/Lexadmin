from backend.repositories.agenda_repository import AgendaRepository


class AgendaService:
    def __init__(self):
        self.repository = AgendaRepository()

    def listar(self):
        return self.repository.list_all()
