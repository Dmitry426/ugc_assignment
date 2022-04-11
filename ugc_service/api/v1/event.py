import logging
from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from ugc_service.services.events import EventSender, get_event_sender
from ugc_service.serializers.kafka import KafkaEventMovieViewTime

from fastapi import APIRouter, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


router = APIRouter()
logger = logging.getLogger(__name__)
http_bearer = HTTPBearer()
security = HTTPBearer(auto_error=False)


@router.post("/event")
async def send_view_progress(
    viewed_progress_data: KafkaEventMovieViewTime,
    event_sender: EventSender = Depends(get_event_sender),
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security),
):
    viewed_progress = KafkaEventMovieViewTime(
        user_uuid=viewed_progress_data.user_uuid,
        movie_id=viewed_progress_data.movie_id,
        event=viewed_progress_data.event
    )
    await event_sender.send_viewed_progress(viewed_progress)
