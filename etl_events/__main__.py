import json

# import backoff
from clickhouse_driver import Client
from kafka import KafkaConsumer
# from kafka.errors import NoBrokersAvailable
from kafka.structs import OffsetAndMetadata
from kafka import TopicPartition


def create_tables(client) -> None:
    print(f'\n\n--12--\n\n')
    client.execute("CREATE DATABASE IF NOT EXISTS movies ON CLUSTER company_cluster;")
    print(f'\n\n--14--создали базу\n\n')
    client.execute(
        """CREATE TABLE IF NOT EXISTS movies.film ON CLUSTER company_cluster(
            user_uuid String,
            movie_id String,
            event Int64,
            created_at Int32
            ) Engine=MergeTree()
            ORDER BY created_at;
     """)
    print(f'\n\n--22-- создали таблицы\n\n')


# @backoff.on_exception(backoff.expo, Exception, max_tries=3)
def insert_clickhouse(client, data: list) -> None:
    print(f'\n\n--29--\n\n')
    client.execute(
        '''
        INSERT INTO film (
        id, user_uuid, movie_id, event, timestamp_movie)  VALUES {}
        '''.format(", ".join("("+i+")" for i in data)))


def etl_process(consumer: KafkaConsumer, clickhouse_client: Client) -> None:
    print(f'\n\n--37--\n\n\n')

    data = []
    print(f'\n\n--40--\n\n\n')
    for msg in consumer:
        print(f'\n\n--35--{msg}\n\n\n')
        data.append((', '.join(json.loads(msg.value.decode('utf-8')).values())))
        if len(data) == 10:
            insert_clickhouse(clickhouse_client, data)
            data.clear()
            tp = TopicPartition("film", msg.partition)
            options = {tp: OffsetAndMetadata(msg.offset + 1, None)}
            consumer.commit(options)
    print(f'\n\n--50--\n\n\n')


# @backoff.on_exception(backoff.expo, NoBrokersAvailable)
def main():
    print(f'\n\n--47-- и снова тут\n\n')
    consumer = KafkaConsumer(
        "film",
        api_version=(0, 11, 5),
        bootstrap_servers=["127.0.0.1:9092"],
        auto_offset_reset="earliest",
        group_id="film",
        enable_auto_commit=False
    )
    print(f'\n\n--55--\n\n')
    clickhouse_client = Client(host="192.168.5.35",
                               port=9000)
    print(f'\n\n--58--\n\n')
    create_tables(clickhouse_client)
    print(f'\n\n--60--\n\n')
    etl_process(consumer, clickhouse_client)
    print(f'\n\n--62--\n\n')


if __name__ == '__main__':
    main()
