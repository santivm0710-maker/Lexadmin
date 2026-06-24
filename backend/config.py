"""Configuración general del backend de LexAdmin.

Este archivo solo define valores de configuración.
Todavía no se conecta a una base de datos real.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "LexAdmin API"
    app_version: str = "0.1.0"
    environment: str = "prototype"

    # Prototipo de variables de conexión.
    # En una versión funcional se podrían leer desde un archivo .env.
    database_driver: str = "postgresql"
    database_host: str = "localhost"
    database_port: int = 5432
    database_name: str = "lexadmin"
    database_user: str = "lexadmin_user"
    database_password: str = "change_me"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
