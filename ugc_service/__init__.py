from fastapi import FastAPI

from ugc_service.api.v1 import ugc

from .core.config import ProjectSettings

base_settings = ProjectSettings()

app = FastAPI(
    title=base_settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
)


@app.on_event("startup")
async def startup():
    pass


@app.on_event("shutdown")
async def shutdown():
    pass


app.include_router(ugc.router, prefix="/api/v1/ugc", tags=["ugc"])
