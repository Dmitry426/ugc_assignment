from datetime import datetime

from pydantic import Field

from .base import JsonConfig


class KafkaEventMovieViewTime(JsonConfig):
    user_uuid: str
    movie_id: str
    event: str
    created: datetime = Field(default_factory=datetime.utcnow)
