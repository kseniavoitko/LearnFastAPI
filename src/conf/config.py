from typing import Any

from pydantic import ConfigDict, field_validator, EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_url: str = (
        "postgresql+psycopg2://user:password@localhost:5432/postgres"
    )
    secret_key: str = "secret_key"
    algorithm: str = "HS256"
    mail_username: EmailStr = "example@meta.ua"
    mail_password: str = "password"
    mail_from: str = "example@meta.ua"
    mail_port: int = 465
    mail_server: str = "smtp.meta.ua"
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: str | None = None
    cloudinary_name: str = 'name'
    cloudinary_api_key: int = 326488457974591
    cloudinary_api_secret: str = 'secret'


    @field_validator("ALGORITHM", check_fields=False)
    @classmethod
    def validate_algorithm(cls, v: Any):
        if v not in ["HS256", "HS512"]:
            raise ValueError("algorithm must be HS256 or HS512")
        return v


    model_config = ConfigDict(extra='ignore', env_file=".env", env_file_encoding="utf-8")


settings = Settings()
