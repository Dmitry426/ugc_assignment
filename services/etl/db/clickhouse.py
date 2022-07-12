__all__ = ["clickhouse_client"]

import logging

import backoff
from clickhouse_driver import Client

from ..core.config import settings

logger = logging.getLogger("ETL_events")


@backoff.on_exception(
    backoff.expo, exception=(RuntimeError, ConnectionError, TimeoutError), max_tries=3
)
def clickhouse_client() -> Client:
    try:
        client = Client(host=settings.c_host, port=settings.c_port)
        logger.info("None - connected to  ClickHouse")
        return client
    except (ConnectionError, RuntimeError) as e:
        logger.error(e, exc_info=True)
