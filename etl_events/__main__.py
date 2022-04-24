from etl_events.core.config import settings
from etl_events.db.clickhouse import clickhouse_client
from etl_events.db.consumer import consumer
from etl_events.services.services import create_tables, etl_process

from etl_events.core.logger import get_logger

logger = get_logger("ETL_events")
logger.info("None - логирование ETL_events началось")

clickhouse_client = clickhouse_client()
consumer = consumer()


def main():
    topic: str = settings.topic
    create_tables(clickhouse_client)
    etl_process(topic, consumer, clickhouse_client)


if __name__ == "__main__":
    main()
