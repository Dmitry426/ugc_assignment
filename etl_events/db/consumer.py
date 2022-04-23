__all__ = ["consumer"]

import logging

import backoff
from kafka import KafkaConsumer

from etl_events.core.config import settings

logger = logging.getLogger("ETL_events")


@backoff.on_exception(
    wait_gen=backoff.expo,
    exception=(RuntimeError, ConnectionError, TimeoutError),
    max_time=settings.k_backoff_timeout,
)
def consumer() -> KafkaConsumer:
    conn: KafkaConsumer = KafkaConsumer(
        settings.topic,
        security_protocol="PLAINTEXT",
        bootstrap_servers=[f"{settings.k_host}:{settings.k_port}"],
        auto_offset_reset="earliest",
        enable_auto_commit=False,
        group_id="$Default",
        value_deserializer=lambda x: x.decode("utf-8"),
        reconnect_backoff_ms=100,
    )
    if conn:
        logger.info(f"X-Request-Id: None: подключился к Kafka")
    else:
        logger.error(f"X-Request-Id: None: не смог подключиться к Kafka")
    return conn
