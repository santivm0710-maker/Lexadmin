from backend.repositories.caso_repository import CasoRepository


class CasoService:
    def __init__(self):
        self.repository = CasoRepository()

    def listar(self):
        return self.repository.list_all()
