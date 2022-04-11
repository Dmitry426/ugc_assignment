import json
import logging

from fastapi import Depends

from ugc_service.db.storage import AbstractEventStorage, get_event_storage
from ugc_service.serializers.kafka import KafkaEventMovieViewTime

logger = logging.getLogger(__name__)


class EventSender:
    def __init__(self, storage: AbstractEventStorage):
        self.storage = storage

    async def send_viewed_progress(self, data: KafkaEventMovieViewTime):
        print(f'\n\n{data}\n\n')
        value = data.toJSON()
        print(f'\n\n{value}\n\n')
        key = f'{data.user_uuid}:{data.movie_id}'.encode()
        print(f'\n\n{key}\n\n')
        await self.storage.send(topic='film', value=value, key=key)


def get_event_sender(
        event_storage: AbstractEventStorage = Depends(get_event_storage),
) -> EventSender:
    return EventSender(storage=event_storage)
