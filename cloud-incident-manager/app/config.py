
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Cloud Incident Manager"

    # Local development and CI can use DATABASE_URL.
    # Production uses DATABASE_SECRET_ARN.
    database_url: str | None = None
    database_secret_arn: str | None = None

    aws_region: str = "us-east-1"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()
