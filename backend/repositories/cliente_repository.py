from backend.entities import Cliente
from backend.repositories.base_repository import BaseRepository


class ClienteRepository(BaseRepository[Cliente]):
    table_name = "clientes"
    entity_class = Cliente
    pk_field = "id_cliente"
