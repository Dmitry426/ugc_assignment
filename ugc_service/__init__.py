from fastapi import FastAPI

from ugc_service.api.v1 import event
from ugc_service.db.storage import get_event_storage, KafkaEventStorage

from .core.config import ProjectSettings

base_settings = ProjectSettings()

app = FastAPI(
    title=base_settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
)


@app.on_event("startup")
async def startup_event():
    await get_event_storage()


@app.on_event("shutdown")
async def shutdown_event():
    event_storage: KafkaEventStorage = await get_event_storage()
    await event_storage.producer.stop()


# app.include_router(ugc.router, prefix="/api/v1/ugc", tags=["ugc"])
app.include_router(event.router, prefix="/api/v1/event", tags=["event"])
