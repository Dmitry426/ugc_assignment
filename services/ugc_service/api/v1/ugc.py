import logging
from http import HTTPStatus
from typing import Optional

from confluent_kafka import KafkaException
from fastapi import APIRouter, Depends, Header, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ...db.producer import get_aio_producer
from ...models.event_message import KafkaEventMovieViewTime
from ...services.base_service import AuthService, KafkaStorage

router = APIRouter()
logger = logging.getLogger("UGC_service")

security = HTTPBearer(auto_error=False)
auth = AuthService()


@router.post(
    "/event",
    name="UGC",
    description="""
Uploads data to Kafka , if success response OK , if error response Error .
JWT token required !
""",
)
async def send_view_progress(
    data: dict,
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security),
    aio_producer: KafkaStorage = Depends(get_aio_producer),
    x_request_id: Optional[str] = Header(None),
):
    token = credentials
    if token:
        payload = auth.decode_token(token=token.credentials, x_request_id=x_request_id)
        user_uuid = payload["user_id"]
    else:
        user_uuid = "guest"

    event = KafkaEventMovieViewTime(user_uuid=user_uuid, **data)
    value_event = event.to_json()
    try:
        await aio_producer.produce("film", value=value_event)
        return HTTPStatus.CREATED
    except KafkaException as kafka_ex:
        logger.error(f"{x_request_id} - Kafka  producing error: {kafka_ex}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=kafka_ex.args[0].str()
        ) from kafka_ex
