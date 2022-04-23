import logging

import uvicorn

from ugc_service import app as application
from ugc_service.core.logger import LOGGING

from .core.config import UvicornSettings

url_settings = UvicornSettings()

uvicorn.run(
    application,
    host=url_settings.host,
    port=url_settings.port,
    log_config=LOGGING,
    log_level=logging.DEBUG,
    proxy_headers=True,
)
