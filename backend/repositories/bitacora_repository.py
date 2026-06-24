from backend.repositories.base_repository import BaseRepository
from backend.repositories.mock_data import BITACORA


class BitacoraRepository(BaseRepository):
    def __init__(self):
        super().__init__(BITACORA)
