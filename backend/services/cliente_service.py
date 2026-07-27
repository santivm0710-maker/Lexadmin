from backend.entities import Cliente
from backend.repositories.cliente_repository import ClienteRepository
from backend.schemas.requests import ClienteCreate


class ClienteService:
    def __init__(self):
        self.repository = ClienteRepository()

    def listar(self):
        return self.repository.list_all()

    def crear(self, datos: ClienteCreate) -> Cliente:
        return self.repository.add(Cliente(id_cliente=0, **datos.model_dump()))

    def actualizar(self, id_cliente: int, datos: ClienteCreate) -> Cliente | None:
        return self.repository.update(id_cliente, Cliente(id_cliente=id_cliente, **datos.model_dump()))

    def eliminar(self, id_cliente: int) -> bool:
        return self.repository.delete(id_cliente)
