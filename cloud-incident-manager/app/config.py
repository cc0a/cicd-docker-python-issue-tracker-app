from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Cloud Incident Manager"
    database_url: str = (
        "postgresql+psycopg://incident:incident@localhost:5432/incidents"
    )

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
