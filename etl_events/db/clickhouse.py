__all__ = ["clickhouse_client"]

import backoff
from clickhouse_driver import Client

from etl_events.core.config import settings


@backoff.on_exception(
    backoff.expo, exception=(RuntimeError, ConnectionError, TimeoutError), max_tries=3
)
def clickhouse_client() -> Client:
    client: Client = Client(host=settings.c_host, port=settings.c_port)
    return client
