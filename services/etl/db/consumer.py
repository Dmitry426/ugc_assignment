__all__ = ["consumer"]

import logging

import backoff
from kafka import KafkaConsumer

from ..core.config import settings

logger = logging.getLogger("ETL_events")


@backoff.on_exception(
    wait_gen=backoff.expo,
    exception=(RuntimeError, ConnectionError, TimeoutError),
    max_time=settings.k_backoff_timeout,
)
def consumer() -> KafkaConsumer:
    try:
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
        logger.info("None - подключился к Kafka")
        return conn
    except (ConnectionError, RuntimeError) as e:
        logger.error(e, exc_info=True)
