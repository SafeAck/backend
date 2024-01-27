from fastapi import APIRouter, Body
from .schemas import UserSchema, UserLoginSchema
from .handler import sign_jwt
from ..config import JWT_EXPIRY

auth_router = APIRouter(
    prefix="/api/v1/auth",
    tags=["auth"],
    redirect_slashes=False
)

users = []


@auth_router.post("/signup")
def signup(user: UserSchema = Body(...)):
    users.append(user)
    return {"msg": "user signed up sucessfully"}


@auth_router.post("/login")
def login(user_data: UserLoginSchema = Body(...)):
    for user in users:
        if user.email == user_data.email and user.password == user_data.password:
            return {"access_token": sign_jwt(user_id=user.email, expiry_minutes=JWT_EXPIRY)}

    return {"msg": "Failed to login! Check email and password!"}
