from datetime import datetime, timedelta
from typing import Annotated
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, SecurityScopes
from fastapi.security.http import HTTPAuthorizationCredentials
from jwt import encode as jwt_encode, decode as jwt_decode
from starlette.requests import Request
from traceback import print_exc
from .permissions import Role, role_based_scopes
from ..config import JWT_ALGORITHM, JWT_SECRET
from ..logger import create_logger
from ..utils.http import get_user_ip

logger = create_logger(__name__)


def sign_jwt(user_id: str, role: str, expiry_minutes: int = 120) -> str | None:
    '''Returns signed token for provided user. Returns None if role is invalid.'''
    token = None

    if role in {m.value for m in Role}:
        current_time = datetime.utcnow()
        payload = {
            "user_id": user_id,
            "iss": "safeack",
            "role": role,
            "iat": current_time,
            "exp": current_time + timedelta(minutes=expiry_minutes),
        }

        token = jwt_encode(payload=payload, algorithm=JWT_ALGORITHM, key=JWT_SECRET)

    return token


def verify_jwt(token: str) -> bool:
    '''Verifies token claims and returns True if claims are
    valid else returns false. If any error occurs then False
    is returned'''
    try:
        decoded_token = jwt_decode(
            jwt=token,
            key=JWT_SECRET,
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
        logger.error('Failed to verify JWT token due to error: %s', repr(e))
        print_exc()
        return False


class JWTBearer(HTTPBearer):
    def __init__(self, *, auto_error: bool = True):
        super(JWTBearer, self).__init__(
            bearerFormat="Bearer Format",
            scheme_name="Bearer",
            description="Bearer JWT Token after logging in",
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        credentials: HTTPAuthorizationCredentials | None = await super().__call__(request)
        client_ip = get_user_ip(request)
        if credentials:
            if credentials.scheme != "Bearer":
                logger.warning(
                    "%s tried to provide invalid http scheme %s",
                    client_ip,
                    credentials.scheme,
                )
                raise HTTPException(status_code=403, detail="Invalid Authentication Scheme")

            if not verify_jwt(credentials.credentials):
                logger.warning("%s provided invalid credentials", client_ip)
                raise HTTPException(status_code=403, detail="Invalid or Expired Token")
            return credentials.credentials
        else:
            logger.warning(
                "%s tried to access %s without proper authentication",
                client_ip,
                request.url,
            )
            raise HTTPException(
                status_code=401,
                detail="Invalid Authorization Token",
            )


def validate_user_perms(security_scopes: SecurityScopes, token=Depends(JWTBearer())) -> int:
    '''validates current user permission and returns user id. Raises exception if current user lack permissions'''
    logger.error(token)
    user_role = token["role"]
    user_id = token["user_id"]
    role_scopes = role_based_scopes[user_role]
    role_scope_keys = role_scopes.keys()

    for scope in security_scopes.scopes:
        if scope not in role_scope_keys:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                # headers={"WWW-Authenticate": authenticate_value},
            )

    return user_id
