from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str

    # Application
    DEBUG: bool = False
    SECRET_KEY: str
    API_VERSION: str = "v1"

    # Logging
    LOG_LEVEL: str = "INFO"

    # Pydantic Settings configuration
    model_config = SettingsConfigDict(
        env_file="backend/.env",
        extra="ignore"
    )

    # Validator for database URL
    @field_validator("DATABASE_URL")
    def check_db_url(cls, v: str) -> str:
        if not v.startswith("postgresql://"):
            raise ValueError("DATABASE_URL must start with 'postgresql://'")
        return v


# Global settings instance
setting = Settings()
