"""Repositorio base prototipo.

La intención de esta capa es aislar el acceso a datos.
Por ahora usa listas de ejemplo y NO base de datos.
"""

from typing import Generic, Iterable, List, TypeVar

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, initial_data: Iterable[T] | None = None):
        self._items: List[T] = list(initial_data or [])

    def list_all(self) -> list[T]:
        return self._items

    def add(self, item: T) -> T:
        self._items.append(item)
        return item
