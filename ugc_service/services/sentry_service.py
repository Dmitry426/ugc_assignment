import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from fastapi import FastAPI


def  setry_app(app:FastAPI)->None:

