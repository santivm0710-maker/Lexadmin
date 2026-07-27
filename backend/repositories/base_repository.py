"""Repositorio base con persistencia en MySQL.

Cada repositorio concreto solo declara su tabla, su entidad y su llave
primaria; toda la lógica de leer/insertar/actualizar/eliminar vive aquí.
"""

import dataclasses
from typing import Generic, Type, TypeVar

from backend.database.connection import DatabaseConnection

T = TypeVar("T")


class BaseRepository(Generic[T]):
    table_name: str = ""
    entity_class: Type[T] = None
    pk_field: str = ""

    # ------------------------------------------------------------------
    def list_all(self) -> list[T]:
        filas = DatabaseConnection.fetch_all(f"SELECT * FROM {self.table_name}")
        return [self.entity_class(**fila) for fila in filas]

    def get_by_id(self, item_id) -> "T | None":
        fila = DatabaseConnection.fetch_one(
            f"SELECT * FROM {self.table_name} WHERE {self.pk_field} = %s", (item_id,)
        )
        return self.entity_class(**fila) if fila else None

    def add(self, item: T) -> T:
        # Se omiten los campos None para que la base de datos aplique sus
        # valores por defecto (fechas automáticas, estados por defecto, etc.).
        datos = self._campos_escribibles(item, incluir_none=False)
        columnas = ", ".join(datos)
        marcadores = ", ".join(["%s"] * len(datos))
        nuevo_id, _ = DatabaseConnection.execute(
            f"INSERT INTO {self.table_name} ({columnas}) VALUES ({marcadores})",
            list(datos.values()),
        )
        return dataclasses.replace(item, **{self.pk_field: nuevo_id})

    def update(self, item_id, item: T) -> "T | None":
        if self.get_by_id(item_id) is None:
            return None
        # En una edición tampoco se sobrescriben con None los campos que el
        # formulario no envía, evitando borrar datos existentes sin querer.
        datos = self._campos_escribibles(item, incluir_none=False)
        asignaciones = ", ".join(f"{col} = %s" for col in datos)
        DatabaseConnection.execute(
            f"UPDATE {self.table_name} SET {asignaciones} WHERE {self.pk_field} = %s",
            list(datos.values()) + [item_id],
        )
        return dataclasses.replace(item, **{self.pk_field: item_id})

    def delete(self, item_id) -> bool:
        _, filas = DatabaseConnection.execute(
            f"DELETE FROM {self.table_name} WHERE {self.pk_field} = %s", (item_id,)
        )
        return filas > 0

    # ------------------------------------------------------------------
    def _campos_escribibles(self, item: T, incluir_none: bool) -> dict:
        datos = dataclasses.asdict(item)
        datos.pop(self.pk_field, None)
        return {
            col: valor
            for col, valor in datos.items()
            if incluir_none or valor is not None
        }
