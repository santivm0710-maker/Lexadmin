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

    def get_by_id(self, item_id) -> T | None:
        connection = DatabaseConnection.connect()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                f"SELECT * FROM {self.table_name} WHERE {self.pk_field} = %s",
                (item_id,),
            )
            row = cursor.fetchone()
            cursor.close()
            return self.entity_class(**row) if row else None
        finally:
            DatabaseConnection.close(connection)

    def update(self, item_id, item: T) -> T | None:
        if self.get_by_id(item_id) is None:
            return None

        data = dataclasses.asdict(item)
        data.pop(self.pk_field, None)
        columns = list(data.keys())
        set_clause = ", ".join([f"{column} = %s" for column in columns])
        values = [data[column] for column in columns] + [item_id]

        connection = DatabaseConnection.connect()
        try:
            cursor = connection.cursor()
            cursor.execute(
                f"UPDATE {self.table_name} SET {set_clause} WHERE {self.pk_field} = %s",
                values,
            )
            connection.commit()
            cursor.close()
            return dataclasses.replace(item, **{self.pk_field: item_id})
        finally:
            DatabaseConnection.close(connection)

    def delete(self, item_id) -> bool:
        connection = DatabaseConnection.connect()
        try:
            cursor = connection.cursor()
            cursor.execute(
                f"DELETE FROM {self.table_name} WHERE {self.pk_field} = %s",
                (item_id,),
            )
            connection.commit()
            eliminado = cursor.rowcount > 0
            cursor.close()
            return eliminado
        finally:
            DatabaseConnection.close(connection)
