import secrets
from typing import Any, List, Tuple, Union

from pydantic import AnyHttpUrl, computed_field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PG_USER: str
    PG_PASS: str
    PG_HOST: str
    PG_DB: str
    PG_PORT: int
    ACCESS_HOURS: int

    KAFKA_HOST: str
    KAFKA_PORT: str
    KAFKA_TOPIC: str
    KAFKA_CONSUMER_GROUP_PREFIX: str

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    @field_validator("BACKEND_CORS_ORIGINS")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str
    ENVIRONMENT: str

    DOCS_ENVIRONMENT: Tuple[str, ...] = ("local", "staging", "development")

    @computed_field
    @property
    def ASYNC_DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.PG_USER}:"
            f"{self.PG_PASS}@"
            f"{self.PG_HOST}:"
            f"{self.PG_PORT}/"
            f"{self.PG_DB}"
        )

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()

app_configs: dict[str, Any] = {
    "title": settings.PROJECT_NAME,
    "openapi_url": None,
}
if settings.ENVIRONMENT in settings.DOCS_ENVIRONMENT:
    app_configs["openapi_url"] = f"{settings.API_V1_STR}/openapi.json"
