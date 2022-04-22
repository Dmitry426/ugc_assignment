import logging

from abc import abstractmethod
from typing import List, Optional

import jwt
from fastapi import HTTPException

logger = logging.getLogger(__name__)


class Auth:
    @property
    @abstractmethod
    def secret_key(self) -> str:
        pass

    @property
    @abstractmethod
    def algorithm(self) -> Optional[List[str]]:
        pass

    def decode_token(self, token: str):
        try:
            payload = jwt.decode(
                jwt=token,
                key=self.secret_key,
                do_verify=True,
                do_time_check=True,
                algorithms=self.algorithm,
            )
            return payload["sub"]

        except jwt.ExpiredSignatureError as ex:
            logger.error(f"X-Request-Id: None: Token expired: {ex}")
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError as ex:
            logger.error(f"X-Request-Id: None: Invalid token: {ex}")
            raise HTTPException(status_code=401, detail="Invalid token")
