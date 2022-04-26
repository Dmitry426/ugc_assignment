import orjson
from pydantic import BaseModel


def orjson_dumps(arg, *, default):
    return orjson.dumps(arg, default=default).decode()


class JsonConfig(BaseModel):
    def to_json(self):
        return orjson.dumps(self, default=lambda o: o.__dict__)

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
