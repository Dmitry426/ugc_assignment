from http import HTTPStatus
from typing import Optional

from aiokafka import AIOKafkaProducer
from fastapi import APIRouter, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.responses import JSONResponse

from ugc_service.core.config import KafkaSettings
from ugc_service.serializers.kafka import KafkaEventMovieViewTime
from ugc_service.services.base_service import AuthService

router = APIRouter()

security = HTTPBearer(auto_error=False)
kafka_settings = KafkaSettings()

auth = AuthService()


@router.post(
    "/data",
    response_model=HTTPStatus,
    name="UGC",
    description="""
    Uploads data to Kafka , if success response OK , if error response Error.
    JWT token required !
    """,
)
async def put_data(
    data: dict,
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security),
):
    token = credentials
    if token:
        payload = auth.decode_token(token=token.credentials)
        user_uuid = payload["user_id"]
    else:
        user_uuid = "anonymus"

    producer = AIOKafkaProducer(
        bootstrap_servers=f"{kafka_settings.host}:{kafka_settings.port}"
    )
    await producer.start()
    event = KafkaEventMovieViewTime(user_uuid=user_uuid, **data)
    try:
        value_event = str.encode(event.event)
        key_event = str.encode(event.user_uuid + event.movie_id)
        await producer.send(
            topic="movies",
            value=value_event,
            key=key_event,
        )
    finally:
        await producer.stop()
    return JSONResponse(status_code=200, content=event)
