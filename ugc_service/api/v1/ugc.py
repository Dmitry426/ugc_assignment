from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from kafka import KafkaProducer

from ugc_service.serializers import KafkaEventMovieViewTime
from ugc_service.services.base_service import AuthService

router = APIRouter()

security = HTTPBearer(auto_error=True)

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
) -> int:
    """
    payload:
    data = {
        movie_id: num,
        event: "00:53:24 до 00:53:25 (1 секунду)",
        created: datatime(optional)
    }
    """
    token = credentials
    if token:
        payload = auth.decode_token(token=token.credentials)
        user_uuid = payload['user_id']
    else:
        user_uuid = 'anonymus'

    event = KafkaEventMovieViewTime(user_uuid=user_uuid, **data)

    # todo примерно так
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
    value_event = str.encode(event.event)
    key_event = str.encode(event.user_uuid + event.movie_id)

    producer.send(
        topic='movies',
        value=value_event,
        key=key_event,
    )

    return HTTPStatus.OK
