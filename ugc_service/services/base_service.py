from abc import ABC

from ugc_service.core.config import JwtSettings
from ugc_service.services.jwt_utils import Auth

jwt = JwtSettings()


class AuthService(Auth, ABC):
    secret_key = jwt.secret_key
    algorithm = jwt.algorithm
