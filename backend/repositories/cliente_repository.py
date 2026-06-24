from backend.repositories.base_repository import BaseRepository
from backend.repositories.mock_data import CLIENTES


class ClienteRepository(BaseRepository):
    def __init__(self):
        super().__init__(CLIENTES)
