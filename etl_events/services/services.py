__all__ = ["create_tables", "etl_process"]

import json
from datetime import datetime

import backoff
from clickhouse_driver import Client
from kafka import KafkaConsumer, TopicPartition
from kafka.structs import OffsetAndMetadata

from etl_events.core.config import settings


@backoff.on_exception(backoff.expo, Exception, max_tries=3)
def create_tables(client: Client) -> None:
    client.execute("CREATE DATABASE IF NOT EXISTS movies ON CLUSTER company_cluster;")
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


@backoff.on_exception(backoff.expo, Exception, max_tries=3)
def insert_clickhouse(client: Client, data: list) -> None:
    values: str = str([i for i in data]).lstrip("[").rstrip("]")
    client.execute(
        """
        INSERT INTO movies.film (
        user_uuid, movie_id, event, created_at)  VALUES {}
        """.format(
            values
        )
    )


@backoff.on_exception(backoff.expo, Exception, max_tries=3)
def etl_process(topic: str, consumer: KafkaConsumer, clickhouse_client: Client) -> None:
    start_interval = datetime.now()
    data: list = []
    for msg in consumer:
        data.append(tuple(json.loads(msg.value).values()))
        td = (datetime.now() - start_interval).total_seconds()
        if len(data) == settings.chunk or td > 300:
            insert_clickhouse(clickhouse_client, data)
            data.clear()
            tp = TopicPartition(topic, msg.partition)
            options = {tp: OffsetAndMetadata(msg.offset + 1, None)}
            consumer.commit(options)
            start_interval = datetime.now()
