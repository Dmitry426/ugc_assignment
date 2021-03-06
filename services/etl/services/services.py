__all__ = ["create_tables", "etl_process"]

import json
import logging
from datetime import datetime

import backoff
from clickhouse_driver import Client
from kafka import KafkaConsumer, TopicPartition
from kafka.structs import OffsetAndMetadata

from ..core.config import settings

logger = logging.getLogger("ETL_events")


@backoff.on_exception(
    backoff.expo, exception=(RuntimeError, ConnectionError, TimeoutError), max_tries=3
)
def create_tables(client: Client) :
    client.execute("CREATE DATABASE IF NOT EXISTS movies ON CLUSTER company_cluster;")
    logger.info("None - DB  created  movies")

    client.execute(
        """CREATE TABLE IF NOT EXISTS movies.film ON CLUSTER company_cluster(
            user_uuid String,
            movie_id String,
            event Int64,
            created_at DateTime64
            ) Engine=MergeTree()
            ORDER BY created_at;
     """
    )
    logger.info("None - table film created ")


@backoff.on_exception(
    backoff.expo, exception=(RuntimeError, ConnectionError, TimeoutError), max_tries=3
)
def insert_clickhouse(client: Client, data: list) :
    values: str = ",".join(map(str, data))

    client.execute(
        f"""
        INSERT INTO movies.film (
        user_uuid, movie_id, event, created_at)  VALUES {values}
        """
    )
    logger.info("None - record inserted into ClickHouse")


@backoff.on_exception(
    backoff.expo, exception=(RuntimeError, ConnectionError, TimeoutError), max_tries=3
)
def etl_process(topic: str, consumer: KafkaConsumer, clickhouse_client: Client) -> None:
    start_interval = datetime.now()
    data: list = []
    for msg in consumer:
        data.append(tuple(json.loads(msg.value).values()))

        time_data = (datetime.now() - start_interval).total_seconds()
        if len(data) == settings.chunk or time_data > 300:
            try:
                count_msg = len(data)

                insert_clickhouse(clickhouse_client, data)

                data.clear()

                topic_partition = TopicPartition(topic, msg.partition)
                options = {topic_partition: OffsetAndMetadata(msg.offset + 1, None)}
                consumer.commit(options)

                logger.info(
                    f"None -  {count_msg}  consumed from   {topic}"
                )
                start_interval = datetime.now()

            except (KeyError, UnicodeEncodeError, ValueError) as e:
                logger.error(e, exc_info=True)
