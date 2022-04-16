__all__ = ["consumer"]

from kafka import KafkaConsumer

from etl_events.core.config import settings

consumer: KafkaConsumer = KafkaConsumer(
    settings.topic,
    security_protocol="PLAINTEXT",
    bootstrap_servers=[f"{settings.k_host}:{settings.k_port}"],
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    group_id="$Default",
    value_deserializer=lambda x: x.decode("utf-8"),
)
