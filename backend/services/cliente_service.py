from backend.entities import Cliente
from backend.repositories.cliente_repository import ClienteRepository
from backend.schemas.requests import ClienteCreate
from backend.services import auditoria

MODULO = "Clientes"


class ClienteService:
    def __init__(self):
        self.repository = ClienteRepository()

    def listar(self):
        return self.repository.list_all()

    def crear(self, datos: ClienteCreate) -> Cliente:
        cliente = self.repository.add(Cliente(**datos.model_dump()))
        auditoria.registrar(MODULO, "Creación", f"Se registró el cliente {cliente.nombre_completo}.")
        return cliente

    def actualizar(self, id_cliente: int, datos: ClienteCreate) -> "Cliente | None":
        cliente = self.repository.update(id_cliente, Cliente(id_cliente=id_cliente, **datos.model_dump()))
        if cliente is not None:
            auditoria.registrar(MODULO, "Actualización", f"Se actualizó el cliente {cliente.nombre_completo}.")
        return cliente

    def eliminar(self, id_cliente: int) -> bool:
        eliminado = self.repository.delete(id_cliente)
        if eliminado:
            auditoria.registrar(MODULO, "Eliminación", f"Se eliminó el cliente con ID {id_cliente}.")
        return eliminado
