import logging
from http import HTTPStatus
from typing import Optional

from confluent_kafka import KafkaException
from fastapi import APIRouter, Depends, HTTPException, Security, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ugc_service.db.storage import AIOProducer, get_aio_producer
from ugc_service.models.kafka import KafkaEventMovieViewTime
from ugc_service.services.base_service import AuthService

router = APIRouter()
logger = logging.getLogger(__name__)

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
    aio_producer: AIOProducer = Depends(get_aio_producer),
    x_request_id: Optional[str] = Header(None),
):
    token = credentials
    if token:
        payload = auth.decode_token(token=token.credentials, x_request_id=x_request_id)
        user_uuid = payload["user_id"]
    else:
        user_uuid = "anonymus"

    event = KafkaEventMovieViewTime(user_uuid=user_uuid, **data)
    value_event = event.toJSON()
    try:
        await aio_producer.produce("film", value=value_event)
        logger.info(f"{x_request_id} - запись в Kafka")
        return HTTPStatus.CREATED
    except KafkaException as ex:
        logger.error(f"{x_request_id} - ошибка записи в Kafka: {ex}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=ex.args[0].str()
        )
