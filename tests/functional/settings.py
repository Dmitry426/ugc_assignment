from pydantic import BaseSettings, Field, SecretStr


class JwtSettings(BaseSettings):
    """Represents JWT settings."""

    class Config:
        env_prefix = "JWT_"

    secret_key: SecretStr = "super-secret-key"
    algorithm: SecretStr = "HS256"


class KafkaSettings(BaseSettings):
    """Represents Kafka settings."""

    class Config:
        env_prefix = "KAFKA_"

    host: str = "127.0.0.1"
    port: str = "9092"
    topic: str = "film"


class ClickSettings(BaseSettings):
    """Represents click settings."""

    class Config:
        env_prefix = "CLICK_"

    host: str = "clickhouse-node1"
    port: str = "8123"


class TestSettings(BaseSettings):
    """Represents Test settings."""

    click: ClickSettings = ClickSettings()
    jwt_settings: JwtSettings = JwtSettings()
    kafka: KafkaSettings = KafkaSettings()
    test_url: str = Field("http://127.0.0.1:4000", env="TEST_URL")
    ping_backoff_timeout: int = Field(30, env="PING_BACKOFF_TIMEOUT")
