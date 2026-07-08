from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "LexAdmin API"
    app_version: str = "0.1.0"
    environment: str = "development"

    database_driver: str = "mysql"
    database_host: str = "localhost"
    database_port: int = 3306
    database_name: str = "lexadmin"
    database_user: str = "root"
    database_password: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()