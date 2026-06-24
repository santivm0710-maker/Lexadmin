from backend.repositories.expediente_repository import ExpedienteRepository


class ExpedienteService:
    def __init__(self):
        self.repository = ExpedienteRepository()

    def listar(self):
        return self.repository.list_all()
