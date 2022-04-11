from kafka import KafkaProducer, KafkaConsumer
# from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from time import sleep


# producer = KafkaProducer(bootstrap_servers=['127.0.0.1:9092'])
#
# producer.send(
#     topic='film',
#     value=b'1611039931',
#     key=b'500271+tt0120338',
# )
print('ну что?')

sleep(1)
print('--15--')
consumer = KafkaConsumer(
    'film',
    bootstrap_servers=['127.0.0.1:9092'],
    auto_offset_reset='earliest',
    group_id='echo-messages-to-stdout',
)
print('--22--')
# print(f'--{len(consumer)}--')

for message in consumer:
    print(f'--25--{message.value}')
print('--25--')
