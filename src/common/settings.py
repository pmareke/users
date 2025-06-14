from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_dsn: str = ""


settings = Settings()
