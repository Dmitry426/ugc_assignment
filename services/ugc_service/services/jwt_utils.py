__all__ = ["Auth"]

import logging
from abc import abstractmethod
from typing import List, Optional

import jwt
from fastapi import HTTPException

logger = logging.getLogger("UGC_service")


class Auth:
    @property
    @abstractmethod
    def secret_key(self) -> str:
        pass

    @property
    @abstractmethod
    def algorithm(self) -> Optional[List[str]]:
        pass

    def decode_token(self, token: str, x_request_id: Optional[str] = None):
        try:
            payload = jwt.decode(
                jwt=token,
                key=self.secret_key,
                do_verify=True,
                do_time_check=True,
                algorithms=self.algorithm,
            )
            return payload["sub"]

        except jwt.ExpiredSignatureError as jwt_expired:
            logger.error(f"{x_request_id} - token expired: {jwt_expired}")
            raise HTTPException(
                status_code=401, detail="Token expired"
            ) from jwt_expired
        except jwt.InvalidTokenError as invalid_token:
            logger.error(f"{x_request_id} - invalid token: {invalid_token}")
            raise HTTPException(
                status_code=401, detail="Invalid token"
            ) from invalid_token
