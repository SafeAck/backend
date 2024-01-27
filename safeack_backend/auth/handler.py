from datetime import datetime, timedelta
from fastapi import HTTPException
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from jwt import encode as jwt_encode, decode as jwt_decode
from starlette.requests import Request
from traceback import print_exc
from ..config import JWT_ALGORITHM, JWT_SECRET
from ..logger import create_logger
from ..utils.http import get_user_ip

logger = create_logger(__name__)


def sign_jwt(user_id: str, expiry_minutes: int = 120) -> str | None:
    '''Returns signed token for provided user'''
    current_time = datetime.utcnow()
    payload = {
        "user_id": user_id,
        "iss": "safeack",
        "iat": current_time,
        "exp": current_time + timedelta(minutes=expiry_minutes),
    }

    token = jwt_encode(
        payload=payload, algorithm=JWT_ALGORITHM, key=JWT_SECRET)

    return token


def verify_jwt(token: str) -> bool:
    '''Verifies token claims and returns True if claims are 
    valid else returns false. If any error occurs then False
    is returned'''
    try:
        decoded_token = jwt_decode(
            jwt=token, key=JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
        )

        if decoded_token["iss"] != "safeack":
            return False

        current_time = datetime.utcnow()
        expiration_time = datetime.fromtimestamp(decoded_token["exp"])
        if current_time >= expiration_time:
            return False

        return True
    except Exception as e:
        logger.error(f'Failed to verify JWT token due to error: {e}')
        print_exc()
        return False


class JWTBearer(HTTPBearer):
    def __init__(self, *, auto_error: bool = True):
        super(JWTBearer, self).__init__(
            bearerFormat="Bearer Format",
            scheme_name="scheme_name",
            description="description",
            auto_error=auto_error
        )

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        credentials: HTTPAuthorizationCredentials | None = await super().__call__(request)
        client_ip = get_user_ip(request)
        if credentials:
            if credentials.scheme != "Bearer":
                logger.warning(
                    f"{client_ip} tried to provide invalid http scheme {credentials.scheme}")
                raise HTTPException(
                    status_code=403,
                    detail="Invalid Authentication Scheme"
                )

            if not verify_jwt(credentials.credentials):
                logger.warning(f"{client_ip} provided invalid credentials")
                raise HTTPException(
                    status_code=403,
                    detail="Invalid or Expired Token"
                )
            return credentials.credentials
        else:
            logger.warning(
                f"{client_ip} tried to access {request.url} without proper authentication"
            )
            raise HTTPException(
                status_code=401,
                detail="Invalid Authorization Token",
            )
