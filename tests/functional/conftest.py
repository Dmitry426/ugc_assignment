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
from settings import TestSettings

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
async def main(settings: TestSettings) -> ChClient:
    async with ClientSession() as s:
        clickhouse = ChClient(
            session=s, url=f"http://{settings.click.host}:{settings.click.port}/"
        )
        await clickhouse.is_alive()
        yield clickhouse
        await clickhouse.close()


@pytest_asyncio.fixture(name="kafka_client", scope="session")
@backoff.on_exception(
    wait_gen=backoff.expo,
    exception=(RuntimeError, ConnectionError, TimeoutError),
    max_time=TestSettings().ping_backoff_timeout,
)
async def send_one(settings: TestSettings) -> AIOKafkaProducer:
    producer = AIOKafkaProducer(
        bootstrap_servers=f"{settings.kafka.host}:{settings.kafka.port}"
    )
    await producer.start()
    yield producer
    await producer.stop()


@pytest_asyncio.fixture(name="http_client", scope="session")
async def http_client_fixture(settings, kafka_client, click_house) -> ClientSession:
    """Represents HTTP client fixture.

    Add dependency fixtures `click_client` and `kafka_client` to
    check they are ready to work.
    """
    async with ClientSession(base_url=settings.test_url) as session:
        yield session


@pytest_asyncio.fixture(name="make_get_request", scope="session")
def make_get_request(http_client: ClientSession):
    """Make HTTP-request"""

    async def inner(
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        jwt: Optional[str] = None,
    ) -> HTTPResponse:
        params = params or {}
        headers = {}
        json = json or {}
        if jwt:
            headers = {"Authorization": "Bearer {}".format(jwt)}

        logger.debug("URL: %s", url)

        async with http_client.request(
            method=method, url=url, params=params, headers=headers, json=json
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
def create_jwt_token(settings: TestSettings) -> jwt:
    payload = {
        "type": "access",
        "exp": datetime.utcnow() + timedelta(days=0, minutes=30),
        "iat": datetime.utcnow(),
        "sub": {"user_id": str(uuid.uuid4())},
    }
    return jwt.encode(
        payload,
        settings.jwt_settings.secret_key,
        algorithm=settings.jwt_settings.algorithm,
    )
