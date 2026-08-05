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

    # En caso de querer importar su propia clave se usa el siguiente comando
    # en la terminal con el venv activado: python -c "import secrets; print(secrets.token_hex(32))"
    jwt_secret_key: str = "e96bbd739d249f8a615d5a8cceb0a9579ef63cab1b6120683f758a24911a03e1"
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutos: int = 480 #8 horas de sesión

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()