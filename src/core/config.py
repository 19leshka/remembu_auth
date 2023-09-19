from typing import List, Union

from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PG_USER: str
    PG_PASS: str
    PG_HOST: str
    PG_DB: str
    PG_PORT: int
    SECRET_KEY: str
    ACCESS_HOURS: int

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
