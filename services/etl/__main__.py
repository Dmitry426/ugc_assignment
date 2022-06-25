from .core.config import settings
from .core.logger import get_logger
from .db.clickhouse import clickhouse_client
from .db.consumer import consumer
from .services.services import create_tables, etl_process

logger = get_logger("ETL_events")
logger.info("Service started ")

clickhouse_client = clickhouse_client()
consumer = consumer()


def main():
    topic: str = settings.topic
    create_tables(clickhouse_client)
    etl_process(topic, consumer, clickhouse_client)


if __name__ == "__main__":
    main()
