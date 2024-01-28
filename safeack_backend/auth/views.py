from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session
from .schemas import UserCreateSchema, UserLoginSchema
from .crud import create_user, get_user_by_email
from .handler import sign_jwt
from .password import verify_password
from ..config import JWT_EXPIRY
from ..database import get_db

auth_router = APIRouter(
    prefix="/api/v1/auth",
    tags=["auth"],
    redirect_slashes=False
)


@auth_router.post("/signup")
def signup(user: UserCreateSchema = Body(...), db: Session = Depends(get_db)):
    user_exists = get_user_by_email(db, user.email)

    if not user_exists and create_user(db, user):
        return {"msg": "user signed up sucessfully"}

    return {"msg": "failed to create user!"}


@auth_router.post("/login")
def login(user_data: UserLoginSchema = Body(...), db: Session = Depends(get_db)):
    user = get_user_by_email(db, user_data.email)
    if user and user.is_active and verify_password(user_data.password, user.hashed_password):
        token = sign_jwt(user.id, JWT_EXPIRY)
        return {"msg": "token generated successfully", "access_token": token}

    return {"msg": "Failed to login! Check email and password!", "access_token": None}
