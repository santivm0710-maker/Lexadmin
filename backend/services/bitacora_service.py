from backend.repositories.bitacora_repository import BitacoraRepository


class BitacoraService:
    def __init__(self):
        self.repository = BitacoraRepository()

    def listar(self):
        return self.repository.list_all()
