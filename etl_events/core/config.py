__all__ = ["settings"]

from pydantic import BaseSettings


class KafkaSettings(BaseSettings):
    """Represents Kafka settings."""

    class Config:
        env_prefix = "ETL_"

    k_host: str = "192.168.5.35"
    k_port: str = "9092"


class ClickHouseSettings(BaseSettings):
    """Represents ClickHouse settings."""

    class Config:
        env_prefix = "ETL_"

    c_host: str = "192.168.5.35"
    c_port: str = "9000"


class Settings(KafkaSettings, ClickHouseSettings):
    """Represents ETL settings."""

    class Config:
        env_prefix = "ETL_"

    topic: str = "film"
    chunk: int = 2


settings = Settings()
