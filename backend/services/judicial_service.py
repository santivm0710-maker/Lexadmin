from backend.repositories.judicial_repository import JudicialRepository


class JudicialService:
    def __init__(self):
        self.repository = JudicialRepository()

    def listar(self):
        return self.repository.list_all()
