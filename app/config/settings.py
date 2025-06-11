from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.services.logger_service import LoggerService

logger = LoggerService()


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="allow"
    )

    environment: str = "development"
    testing: bool = False

    # JWT settings
    secret_key: str = "a_very_secret_key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Database settings
    db_host: str = "192.168.1.135"
    db_port: int = 5432
    db_name: str = "consume_nacional"
    db_user: str = "postgres"
    db_password: str = "password"

    # Blob storage settings
    blob_url: str = "https://bucket.lucantel.es/consume-images/"

    @property
    def database_url(self) -> str:
        """Gets the database URL.

        Returns:
            str: Database URL
        """
        postgres_url = f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
        logger.log(
            entry={
                "message": "Database connection URL",
                "url": postgres_url.replace(
                    self.db_password, "****"
                ),  # Ocultamos la contraseña por seguridad
            },
            filename="database",
        )
        return postgres_url


@lru_cache
def get_settings() -> Settings:
    """Gets application settings.

    Returns:
        Settings: Application settings instance

    Raises:
        ValueError: If OpenAI or Google configuration is invalid
    """
    settings = Settings()  # type: ignore[call-arg]
    return settings
