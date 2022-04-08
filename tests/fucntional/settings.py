from pydantic import BaseSettings, Field

from ugc_service.core.config import JwtSettings, KafkaSettings


class ClickSettings(BaseSettings):
    """Represents click settings."""

    class Config:
        env_prefix = "CLICK_"

    host: str = "clickhouse-node1"
    port: str = "8123"


class TestSettings(BaseSettings):
    """Represents Test settings."""

    jwt_settings: JwtSettings = JwtSettings()
    kafka: KafkaSettings = KafkaSettings()
    test_url: str = Field("http://127.0.0.1:4000", env="TEST_URL")
    ping_backoff_timeout: int = Field(30, env="PING_BACKOFF_TIMEOUT")
