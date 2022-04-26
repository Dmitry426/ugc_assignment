__all__ = ["AuthService", "KafkaStorage"]

from abc import ABC

from ugc_service.core.config import JwtSettings, KafkaSettings
from ugc_service.services.jwt_utils import Auth
from ugc_service.services.kafka_utils import AIOProducer

jwt = JwtSettings()
kafka_settings = KafkaSettings()

config = {"bootstrap.servers": f"{kafka_settings.host}:{kafka_settings.port}"}


class AuthService(Auth, ABC):
    secret_key = jwt.secret_key.get_secret_value()
    algorithm = jwt.algorithm.get_secret_value()


class KafkaStorage(AIOProducer):
    configs = config
