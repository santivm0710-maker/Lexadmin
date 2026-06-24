from backend.repositories.cliente_repository import ClienteRepository


class ClienteService:
    def __init__(self):
        self.repository = ClienteRepository()

    def listar(self):
        return self.repository.list_all()
