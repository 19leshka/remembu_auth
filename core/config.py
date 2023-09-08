from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    PG_USER: str
    PG_PASS: str
    PG_HOST: str
    PG_DB: str
    PG_PORT: int
    SECRET_KEY: str
    ACCESS_HOURS: int


settings = Settings()
