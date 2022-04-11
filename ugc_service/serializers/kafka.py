from datetime import datetime

from pydantic import Field

from .base import JsonConfig

from uuid import UUID


class KafkaEventMovieViewTime(JsonConfig):
    user_uuid: UUID or str
    movie_id: UUID or str
    event: int or str
    # created: datetime = Field(default_factory=datetime.utcnow)
