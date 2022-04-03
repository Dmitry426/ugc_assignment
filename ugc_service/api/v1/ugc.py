from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

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

    return HTTPStatus.OK
