import abc
import asyncio
import logging
from typing import Optional

from aiokafka import AIOKafkaProducer
from ugc_service.core.config import KafkaSettings

kafka_settings = KafkaSettings()


class AbstractEventStorage(abc.ABC):
    @abc.abstractmethod
    def send(self, *args, **kwargs):
        pass


logger = logging.getLogger(__name__)


class KafkaEventStorage(AbstractEventStorage):
    def __init__(self, producer: AIOKafkaProducer):
        self.producer = producer

    async def send(self, topic: str, value: str, key: str, *args, **kwargs):
        try:
            print(f'Sending {topic}, {key}, {value}')
            result = await self.producer.send_and_wait(topic=topic, value=value, key=key)
            # massage = await result
            # print(f"30\n\n{massage}\n\n")
            print(f"31\n\n{result.offset}\n\n")
        except Exception as e:
            logger.exception(e)


event_storage: Optional[AbstractEventStorage] = None


async def get_event_storage() -> AbstractEventStorage:
    global event_storage
    if not event_storage:
        loop = asyncio.get_event_loop()
        kafka_producer = AIOKafkaProducer(
            loop=loop,
            bootstrap_servers=f"{kafka_settings.host}:{kafka_settings.port}"
        )
        await kafka_producer.start()
        event_storage = KafkaEventStorage(producer=kafka_producer)
    return event_storage
