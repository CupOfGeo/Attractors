import enum
from pathlib import Path
from tempfile import gettempdir

from pydantic_settings import BaseSettings

TEMP_DIR = Path(gettempdir())


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Environment(str, enum.Enum):
    LOCAL = "LOCAL"
    DEV = "DEV"
    PROD = "PROD"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    host: str = "0.0.0.0"
    port: int = 8080
    # quantity of workers for uvicorn
    workers_count: int = 1
    # Enable uvicorn reloading
    reload: bool = False

    # Current environment
    environment: Environment = Environment.DEV

    backend_cors_origins: list = []

    log_level: LogLevel = LogLevel.INFO

    backend_url = "https://attractors-service-c6dyl3tniq-uc.a.run.app"

    class Config:
        env_file = ".env"
        env_prefix = "APP_"
        env_file_encoding = "utf-8"


settings = Settings()
