from datetime import datetime
from pydantic import Field

from typing import Union

from .base import JsonConfig


class KafkaEventMovieViewTime(JsonConfig):
    user_uuid: str
    movie_id: str
    event: Union[str, int]
    created: datetime = Field(default_factory=datetime.utcnow)

