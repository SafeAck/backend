from typing import Annotated
from fastapi import APIRouter, Body, Depends, status, HTTPException
from fastapi.security import SecurityScopes, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .schemas import UserCreateSchema, UserLoginSchema, TokenResponseSchema
from .crud import create_user, get_user_by_email
from .permissions import superuser_permissions, role_based_scopes
from .handler import sign_jwt, create_oauth_jwt
from .password import verify_password
from ..config import JWT_EXPIRY
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
def signup(user: UserCreateSchema = Body(...), db: Session = Depends(get_db)):
    user_exists = get_user_by_email(db, user.email)

    if not user_exists and create_user(db, user):
        return {"msg": "user signed up sucessfully"}

    return {"msg": "failed to create user!"}


@auth_router.post("/token")
def login(
    user_data: UserLoginSchema = Body(...), db: Session = Depends(get_db)
) -> TokenResponseSchema:
    msg = "Failed to login! Check email and password!"
    token = None
    user = get_user_by_email(db, user_data.email)
    if user and user.is_active and verify_password(user_data.password, user.hashed_password):
        token = sign_jwt(user.id, user.role, JWT_EXPIRY)
        print(token)
        if token:
            msg = "token generated successfully"

    return TokenResponseSchema(msg=msg, access_token=token)


@auth_router.post(oauth_login_uri)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)
) -> TokenResponseSchema:
    email = form_data.username
    password = form_data.password

    msg = "Failed to login! Check email and password!"
    token = None
    user = get_user_by_email(db, email)
    # if user and user.is_active and verify_password(password, user.hashed_password):
    if user and verify_password(
        password, user.hashed_password
    ):  # TODO: check if user is active or not
        token = create_oauth_jwt(user.id, user.role, JWT_EXPIRY)
        if token:
            msg = "token generated successfully"

    return TokenResponseSchema(msg=msg, access_token=token)


def validate_user_perms(
    security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme, use_cache=False)]
) -> int:
    '''validates current user permission and returns user id. Raises exception if current user lack permissions'''
    logger.info('test')
    print(token)
    user_role = token["role"]
    user_id = int(token["user_id"])
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
