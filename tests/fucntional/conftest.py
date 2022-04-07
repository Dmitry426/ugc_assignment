import asyncio
import logging
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import backoff as backoff
import jwt
import pytest
import pytest_asyncio
from aiochclient import ChClient
from aiohttp import ClientSession
from aiokafka import AIOKafkaProducer
from pydantic import BaseModel

from tests.fucntional.settings import TestSettings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class HTTPResponse(BaseModel):
    body: Any
    headers: Dict[str, Any]
    status: int


@pytest_asyncio.fixture(name="settings", scope="session")
def settings_fixture() -> TestSettings:
    return TestSettings()


@pytest_asyncio.fixture(name="click_house", scope="session")
@backoff.on_exception(
    wait_gen=backoff.expo,
    exception=(RuntimeError, ConnectionError, TimeoutError),
    max_time=TestSettings().ping_backoff_timeout,
)
async def main():
    async with ClientSession() as s:
        clickhouse = ChClient(s)
        await clickhouse.is_alive()
        yield clickhouse
        await clickhouse.close()


@pytest_asyncio.fixture(name="kafka_client", scope="session")
@backoff.on_exception(
    wait_gen=backoff.expo,
    exception=(RuntimeError, ConnectionError, TimeoutError),
    max_time=TestSettings().ping_backoff_timeout,
)
async def send_one():
    producer = AIOKafkaProducer(bootstrap_servers="localhost:9092")
    await producer.start()
    yield producer
    await producer.stop()


@pytest_asyncio.fixture(name="http_client", scope="session")
async def http_client_fixture(settings, kafka_client, click_house) -> ClientSession:
    """Represents HTTP client fixture.

    Add dependency fixtures `click_client` and `kafka_client` to
    check they are ready to work.
    """
    async with ClientSession(
        base_url=f"http://{settings.url_settings.host}:{settings.url_settings.port}"
    ) as session:
        yield session


@pytest_asyncio.fixture(name="make_get_request", scope="session")
def make_get_request(http_client: ClientSession):
    """Make HTTP-request"""

    async def inner(
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        jwt: Optional[str] = None,
    ) -> HTTPResponse:
        params = params or {}
        headers = {}

        if jwt:
            headers = {"Authorization": "Bearer {}".format(jwt)}

        logger.debug("URL: %s", url)

        async with http_client.request(
            method=method, url=url, params=params, headers=headers
        ) as response:
            body = await response.json()
            logger.warning("Response: %s", body)

            return HTTPResponse(
                body=body,
                headers=dict(response.headers),
                status=response.status,
            )

    return inner


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(name="create_jwt_token", scope="function")
def create_jwt_token(settings: TestSettings):
    payload = {
        "type": "access",
        "exp": datetime.utcnow() + timedelta(days=0, minutes=30),
        "iat": datetime.utcnow(),
        "sub": {"user_id": uuid.uuid4()},
    }
    return jwt.encode(
        payload,
        settings.jwt_settings.secret_key,
        algorithm=settings.jwt_settings.algorithm,
    )
