__all__ = ["KafkaEventMovieViewTime"]

from datetime import datetime
from typing import Union

from pydantic import Field

from .base import JsonConfig


class KafkaEventMovieViewTime(JsonConfig):
    user_uuid: str
    movie_id: str
    event: Union[str, int]
    created: datetime = Field(default_factory=datetime.utcnow)
