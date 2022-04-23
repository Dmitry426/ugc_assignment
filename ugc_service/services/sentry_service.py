import sentry_sdk
from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from ugc_service.core.config import CentrySettings

sentry_settings = CentrySettings()


def setry_app(app: FastAPI) -> None:
    sentry_sdk.init(
        dsn=sentry_settings.dsn.get_secret_value(),
        traces_sample_rate=sentry_settings.traces_sample_rate,
    )
    SentryAsgiMiddleware(app)
