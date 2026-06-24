from backend.repositories.base_repository import BaseRepository
from backend.repositories.mock_data import INFO_JUDICIAL


class JudicialRepository(BaseRepository):
    def __init__(self):
        super().__init__(INFO_JUDICIAL)
