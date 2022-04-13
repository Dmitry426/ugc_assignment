import backoff
import json

from clickhouse_driver import Client
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
from kafka.structs import OffsetAndMetadata
from kafka import TopicPartition

from config import settings


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
     """)


@backoff.on_exception(backoff.expo, Exception, max_tries=3)
def insert_clickhouse(client: Client, data: list) -> None:
    values: str = str([i for i in data]).lstrip('[').rstrip(']')
    client.execute(
        '''
        INSERT INTO movies.film (
        user_uuid, movie_id, event, created_at)  VALUES {}
        '''.format(values)
    )


def etl_process(topic: str, consumer: KafkaConsumer, clickhouse_client: Client) -> None:
    data: list = []
    for msg in consumer:
        data.append(tuple(json.loads(msg.value).values()))
        if len(data) == 2:
            insert_clickhouse(clickhouse_client, data)
            data.clear()
            tp = TopicPartition(topic, msg.partition)
            options = {tp: OffsetAndMetadata(msg.offset + 1, None)}
            consumer.commit(options)


@backoff.on_exception(backoff.expo, NoBrokersAvailable)
def main():
    topic: str = settings.topic
    consumer = KafkaConsumer(
        topic,
        security_protocol="PLAINTEXT",
        bootstrap_servers=[f"{settings.k_host}:{settings.k_port}"],
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="$Default",
        value_deserializer=lambda x: x.decode("utf-8")
    )
    clickhouse_client: Client = Client(
        host=settings.c_host,
        port=settings.c_port
    )
    create_tables(clickhouse_client)
    etl_process(topic, consumer, clickhouse_client)


if __name__ == '__main__':
    main()
