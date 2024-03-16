from typing import Annotated
from fastapi import Body, Depends, Security, HTTPException, APIRouter, status
from fastapi.security import SecurityScopes, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from . import MePerm
from .schemas import UserCreateSchema, UserLoginSchema, TokenResponseSchema, UserScannerTokenSchema
from .crud import create_user, get_user_by_email, get_user_active_status
from .permissions import superuser_permissions, role_based_scopes
from .handler import sign_jwt, create_oauth_jwt, jwt_decode, JWTBearer
from .password import verify_password
from ..config import JWT_EXPIRY, JWT_ALGORITHM, JWT_SECRET
from ..database import get_db
from ..logger import create_logger


logger = create_logger(__name__)

auth_url_prefix = "/api/v1/auth"
oauth_login_uri = "/oauth/login"

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{auth_url_prefix}{oauth_login_uri}",
    scopes=superuser_permissions,
)

auth_router = APIRouter(prefix=auth_url_prefix, tags=["auth"], redirect_slashes=False)


@auth_router.post("/signup")
async def signup(user: UserCreateSchema = Body(...), db: Session = Depends(get_db)):
    user_exists = get_user_by_email(db, user.email)

    if not user_exists and create_user(db, user):
        return {"msg": "user signed up sucessfully"}

    return {"msg": "failed to create user!"}


@auth_router.post("/token")
async def login(
    user_data: UserLoginSchema = Body(...), db: Session = Depends(get_db)
) -> TokenResponseSchema:
    """
    Generate auth token for user using email and password
    """
    msg = "Failed to login! Check email and password!"
    token = None
    user = get_user_by_email(db, user_data.email)
    if user and user.is_active and verify_password(user_data.password, user.hashed_password):
        token = sign_jwt(user.id, user.role, JWT_EXPIRY)
        if token:
            msg = "token generated successfully"

    return TokenResponseSchema(msg=msg, access_token=token)


@auth_router.post(oauth_login_uri)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)
) -> TokenResponseSchema:
    email = form_data.username
    password = form_data.password
    scopes = form_data.scopes

    msg = "Failed to login! Check email and password!"
    token = None
    user = get_user_by_email(db, email)

    if user and user.is_active and verify_password(password, user.hashed_password):
        valid_scopes = list(set(scopes) & set(role_based_scopes[user.role.value].keys()))
        token = create_oauth_jwt(user.id, user.role, valid_scopes, JWT_EXPIRY)
        if token:
            msg = "token generated successfully"

    return TokenResponseSchema(msg=msg, access_token=token)


def validate_user_perms(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme, use_cache=True)]
    or Annotated[str, Depends(JWTBearer(), use_cache=True)],
) -> int:
    '''validates current user permission and returns user id. Raises exception if current user lack permissions'''
    try:
        decoded_token = jwt_decode(
            jwt=token,
            key=JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
        )
    except Exception as e:
        logger.error("Error occurred while validating token %s due to error: %s", token, e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
        )

    user_role = decoded_token["role"]
    user_id = int(decoded_token["user_id"])

    # for oauth
    role_scopes = decoded_token.get("scope", None)
    role_scope_keys = role_scopes

    # if no scope found in token then fallback to RBAC perms
    if not role_scopes:
        role_scopes = role_based_scopes[user_role]
        role_scope_keys = list(role_scopes.keys())

    for scope in security_scopes.scopes:
        if scope not in role_scope_keys:
            logger.warning('user id %d tried to access unauthorized data', user_id)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
            )

    return user_id


@auth_router.post("/scan-token")
async def generate_scanner_token(
    user_id: Annotated[int, Security(validate_user_perms, scopes=[MePerm.WRITE_RESULTS.value])],
    data: UserScannerTokenSchema = Body(...),
    db: Session = Depends(get_db),
) -> TokenResponseSchema:
    """
    Generates JWT token for SafeACK Scanner
    """
    msg = "User is inactive"
    token = None

    is_active, role = get_user_active_status(db=db, user_id=user_id)
    if is_active and role:
        msg = "Scanner Auth Token Generated Successfully"
        token = create_oauth_jwt(
            user_id=user_id,
            role=role,
            expiry_minutes=data.expiry_minutes,
            scopes=[MePerm.WRITE_RESULTS.value],
        )

    return TokenResponseSchema(msg=msg, access_token=token)
