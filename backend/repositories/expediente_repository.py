from backend.repositories.base_repository import BaseRepository
from backend.repositories.mock_data import EXPEDIENTES


class ExpedienteRepository(BaseRepository):
    def __init__(self):
        super().__init__(EXPEDIENTES)
