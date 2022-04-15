import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class JsonConfig(BaseModel):
    def toJSON(self):
        return orjson.dumps(self, default=lambda o: o.__dict__)

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
