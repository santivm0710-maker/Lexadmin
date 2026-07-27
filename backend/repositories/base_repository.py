"""Repositorio base con persistencia real en MySQL."""

import dataclasses
from typing import Generic, Type, TypeVar

from backend.database.connection import DatabaseConnection

T = TypeVar("T")


class BaseRepository(Generic[T]):
    table_name: str = ""
    entity_class: Type[T] = None
    pk_field: str = ""

    def list_all(self) -> list[T]:
        connection = DatabaseConnection.connect()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(f"SELECT * FROM {self.table_name}")
            rows = cursor.fetchall()
            cursor.close()
            return [self.entity_class(**row) for row in rows]
        finally:
            DatabaseConnection.close(connection)

    def add(self, item: T) -> T:
        data = dataclasses.asdict(item)
        data.pop(self.pk_field, None)
        columns = list(data.keys())
        placeholders = ", ".join(["%s"] * len(columns))
        values = [data[column] for column in columns]

        connection = DatabaseConnection.connect()
        try:
            cursor = connection.cursor()
            cursor.execute(
                f"INSERT INTO {self.table_name} ({', '.join(columns)}) VALUES ({placeholders})",
                values,
            )
            connection.commit()
            new_id = cursor.lastrowid
            cursor.close()
            return dataclasses.replace(item, **{self.pk_field: new_id})
        finally:
            DatabaseConnection.close(connection)
