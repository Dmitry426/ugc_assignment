__all__ = ["clickhouse_client"]

import logging

import backoff
from clickhouse_driver import Client

from etl_events.core.config import settings

logger = logging.getLogger("ETL_events")


@backoff.on_exception(
    backoff.expo, exception=(RuntimeError, ConnectionError, TimeoutError), max_tries=3
)
def clickhouse_client() -> Client:
    client: Client = Client(host=settings.c_host, port=settings.c_port)
    if client:
        logger.info("X-Request-Id: None: подключился к ClickHouse")
    else:
        logger.error("X-Request-Id: None: не смог подключиться к ClickHouse")
    return client
