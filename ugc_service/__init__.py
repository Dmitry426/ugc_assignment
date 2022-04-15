from fastapi import Depends, FastAPI

from ugc_service.api.v1 import ugc

from .core.config import KafkaSettings, ProjectSettings
from .db.storage import get_aio_producer
from .services.kafka_unit_producer import AIOProducer

base_settings = ProjectSettings()
kafka_settings = KafkaSettings()
app = FastAPI(
    title=base_settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
)


@app.on_event("startup")
async def startup_event(aio_producer: AIOProducer = Depends(get_aio_producer)):
    pass


@app.on_event("shutdown")
def shutdown_event(aio_producer: AIOProducer = Depends(get_aio_producer)):
    aio_producer.close()


app.include_router(ugc.router, prefix="/api/v1/ugc", tags=["ugc"])
