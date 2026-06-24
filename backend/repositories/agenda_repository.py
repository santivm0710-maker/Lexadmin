from backend.repositories.base_repository import BaseRepository
from backend.repositories.mock_data import AGENDA


class AgendaRepository(BaseRepository):
    def __init__(self):
        super().__init__(AGENDA)
