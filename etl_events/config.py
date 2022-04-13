from pydantic import BaseSettings


class Settings(BaseSettings):
    """Represents ETL settings."""

    class Config:
        env_prefix = "ETL_"

    k_host: str = "192.168.5.35"
    k_port: str = "9092"
    c_host: str = "192.168.5.35"
    c_port: str = "9000"
    topic: str = "film"


settings = Settings()
