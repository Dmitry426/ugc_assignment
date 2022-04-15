__all__ = ["clickhouse_client"]

from clickhouse_driver import Client

from etl_events.core.config import settings

clickhouse_client: Client = Client(host=settings.c_host, port=settings.c_port)
