import logging
from http import HTTPStatus

import pytest

logger = logging.getLogger(__name__)

pytestmark = pytest.mark.asyncio

PATH = "/api/v1/ugc"


class TestUserAuth:
    data = {"movie_id": "sfsdf", "event": "sdfsadf"}

    async def test_post_data(self, make_get_request, create_jwt_token):
        response = await make_get_request(
            method="POST",
            url=f"{PATH}/event",
            json=self.data,
            jwt_token=create_jwt_token,
        )
        assert response.status == HTTPStatus.OK
        logger.info("None - Response status : %s", response.status)
