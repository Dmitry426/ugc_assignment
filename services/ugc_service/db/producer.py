__all__ = ["get_aio_producer"]

import logging
from typing import Optional

import backoff

from ..core.config import ProjectSettings
from ..services.base_service import KafkaStorage

logger = logging.getLogger("UGC_service")

project_settings = ProjectSettings()

aio_producer: Optional[KafkaStorage] = None


@backoff.on_exception(
    wait_gen=backoff.expo,
    exception=(RuntimeError, ConnectionError, TimeoutError),
    max_time=project_settings.ping_backoff_timeout,
)
async def get_aio_producer() -> Optional[KafkaStorage]:
    global aio_producer
    aio_producer = KafkaStorage()
    return aio_producer
