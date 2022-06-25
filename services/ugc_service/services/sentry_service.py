__all__ = ["sentry_app"]

import logging

import sentry_sdk
from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from ..core.config import CentrySettings

sentry_settings = CentrySettings()
logger = logging.getLogger(__name__)


def sentry_app(app: FastAPI) :
    if sentry_settings.dsn.get_secret_value():
        sentry_sdk.init(
            dsn=sentry_settings.dsn.get_secret_value(),
            traces_sample_rate=sentry_settings.traces_sample_rate,
        )
        SentryAsgiMiddleware(app)
        logger.info("None - Sentry middleware initialized ")
    else:
        logger.info("None - Sentry dsn not present  ")
