from typing import Optional

import backoff
import logging

from ugc_service.core.config import KafkaSettings, ProjectSettings
from ugc_service.services.kafka_unit_producer import AIOProducer

logger = logging.getLogger("UGC_service")

kafka_settings = KafkaSettings()
project_settings = ProjectSettings()

config = {"bootstrap.servers": f"{kafka_settings.host}:{kafka_settings.port}"}

aio_producer: Optional[AIOProducer] = None


@backoff.on_exception(
    wait_gen=backoff.expo,
    exception=(RuntimeError, ConnectionError, TimeoutError),
    max_time=project_settings.ping_backoff_timeout,
)
async def get_aio_producer() -> AIOProducer:
    global aio_producer
    aio_producer = AIOProducer(config)
    return aio_producer
