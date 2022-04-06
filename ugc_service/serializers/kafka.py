from datetime import datetime

import orjson
from pydantic import BaseModel, Field


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class ConfiguredBaseConfig(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class KafkaEventMovieViewTime(ConfiguredBaseConfig):
    user_uuid: str
    movie_id: str or int
    event: str
    created: datetime = Field(default_factory=datetime.utcnow)
