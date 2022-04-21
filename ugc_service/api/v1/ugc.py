import logging
from http import HTTPStatus
from typing import Optional

from confluent_kafka import KafkaException
from fastapi import APIRouter, Depends, HTTPException, Security, Request
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
Uploads data to Kafka , if success response OK , if error response Error.
JWT token required !
""",
)
async def send_view_progress(
    req: Request,
    data: dict,
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security),
    aio_producer: AIOProducer = Depends(get_aio_producer),
):
    token = credentials
    if token:
        payload = auth.decode_token(token=token.credentials)
        user_uuid = payload["user_id"]
    else:
        user_uuid = "anonymus"
    x_request_id = req.headers.get('x-request-id')

    event = KafkaEventMovieViewTime(user_uuid=user_uuid, **data)
    value_event = event.to_json()
    try:
        await aio_producer.produce("film", value=value_event)
        logger.info(f"Запись в Kafka, X-Request-Id: {x_request_id}")
        return HTTPStatus.CREATED
    except KafkaException as ex:
        logger.error(f"Ошибка записи в Kafka (X-Request-Id: {x_request_id}): {ex}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=ex.args[0].str()
        )
