from .base import JsonConfig


class KafkaEventMovieViewTime(JsonConfig):
    user_uuid: str
    movie_id: str
    event: str or int
