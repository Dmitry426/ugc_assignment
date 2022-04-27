__all__ = ["app"]

import logging.config

from fastapi import Depends, FastAPI

from ugc_service.api.v1 import ugc

from .core.config import KafkaSettings, ProjectSettings
from .core.logger import LOGGING
from .db.storage import get_aio_producer
from .services.kafka_utils import AIOProducer
from .services.sentry_service import sentry_app

logging.config.dictConfig(LOGGING)
logger = logging.getLogger("UGC_service")
logger.info("None - Логирование UGC началось")

base_settings = ProjectSettings()
kafka_settings = KafkaSettings()
app = FastAPI(
    title=base_settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
)

sentry_app(app)


@app.on_event("startup")
async def startup_event():
    pass


@app.on_event("shutdown")
def shutdown_event(aio_producer: AIOProducer = Depends(get_aio_producer)):
    aio_producer.close()


app.include_router(ugc.router, prefix="/api/v1/ugc", tags=["ugc"])
