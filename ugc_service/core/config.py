__all__ = ["JwtSettings", "UvicornSettings", "ProjectSettings", "KafkaSettings"]

import os

from pydantic import BaseSettings


class UvicornSettings(BaseSettings):
    """Represents uvicorn settings."""

    class Config:
        env_prefix = "UVICORN_"

    host: str = "127.0.0.1"
    port: str = "4000"


class JwtSettings(BaseSettings):
    """Represents JWT settings."""

    class Config:
        env_prefix = "JWT_"

    secret_key: str = "super-secret-key"
    algorithm: str = "HS256"


class ProjectSettings(BaseSettings):
    """Represents Project settings."""

    class Config:
        env_prefix = "PROJECT_"

    base_dir: str = os.path.dirname(os.path.abspath(__file__))
    project_name: str = "UGC"
    ping_backoff_timeout: int = 30


class KafkaSettings(BaseSettings):
    """Represents Kafka settings."""

    class Config:
        env_prefix = "KAFKA_"

    host: str = "kafka"
    port: str = "9092"
    topic: str = "film"
