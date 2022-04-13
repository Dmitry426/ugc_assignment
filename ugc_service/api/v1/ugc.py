import logging

from typing import Optional

from fastapi import Depends

from starlette.responses import JSONResponse

from ugc_service.models.kafka import KafkaEventMovieViewTime
from ugc_service.services.base_service import AuthService
from ugc_service.services.kafka_producer import EventSender, get_event_sender


from fastapi import APIRouter, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

router = APIRouter()
logger = logging.getLogger(__name__)

http_bearer = HTTPBearer()

security = HTTPBearer(auto_error=False)
auth = AuthService()


@router.post("/event",
             name="UGC",
             description="""
Uploads data to Kafka , if success response OK , if error response Error.
JWT token required !
""",
)
async def send_view_progress(
    data: dict,
    event_sender: EventSender = Depends(get_event_sender),
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security),
):
    token = credentials
    if token:
        payload = auth.decode_token(token=token.credentials)
        user_uuid = payload["user_id"]
    else:
        user_uuid = "anonymus"

    event = KafkaEventMovieViewTime(user_uuid=user_uuid, **data)
    await event_sender.send_viewed_progress(event)
    return JSONResponse(
        status_code=200,
    )
