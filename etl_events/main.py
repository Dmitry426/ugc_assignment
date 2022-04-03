"""Это черновик"""

from kafka import KafkaConsumer


def get_consumer():
    consumer = KafkaConsumer(
        'movies',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        group_id='echo-messages-to-stdout',
    )
    return consumer


def get_messages(consumer: KafkaConsumer):
    # todo тут получение сообщений. Можно сделать через генератор
    for message in consumer:
        print(message.value)


if __name__ == '__main__':
    # 1. запускаем konsumer
    consumer = get_consumer()
    # 2. читаем сообщения
    get_messages(consumer)
