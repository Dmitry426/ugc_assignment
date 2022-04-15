import backoff

from clickhouse_driver import Client
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

from etl_events.core.config import settings
from etl_events.services.services import create_tables, etl_process
from etl_events.db.clickhouse import clickhouse_client
from etl_events.db.consumer import consumer


@backoff.on_exception(backoff.expo, NoBrokersAvailable)
def main():
    topic: str = settings.topic
    create_tables(clickhouse_client)
    etl_process(topic, consumer, clickhouse_client)


if __name__ == '__main__':
    main()
