'''
FastAPI schemas
'''

from fastapi import HTTPException
from pydantic import BaseModel, Field, EmailStr, field_validator
from ..utils.regex import regexs


class UserBase(BaseModel):
    email: EmailStr = Field(...)


class UserSchema(UserBase):
    full_name: str = Field(..., min_length=4, max_length=100)
    first_name: str = Field(..., min_length=2, max_length=30)
    last_name: str = Field(..., min_length=2, max_length=30)

    @field_validator("first_name")
    def validate_fname(cls, value):
        if not regexs["name"].match(value):
            raise HTTPException(
                status_code=400,
                detail="first name can only contain smallcase and uppercase characters",
            )

        return value

    @field_validator("last_name")
    def validate_lname(cls, value):
        if not regexs["name"].match(value):
            raise HTTPException(
                status_code=400,
                detail="last name can only contain smallcase and uppercase characters",
            )

        return value

    @field_validator("full_name")
    def validate_full_name(cls, value):
        if not regexs["full_name"].match(value):
            raise HTTPException(
                status_code=400,
                detail="full name can only contain smallcase, uppercase and space characters",
            )

        return value

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "full_name": "John Doe",
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "password": "ExamPL3P4$$W0rD!!0194",
            }
        }


class UserCreateSchema(UserSchema):
    password: str = Field(..., min_length=15, max_length=100)


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(..., min_length=15, max_length=100)

    class Config:
        json_schema_extra = {
            "example": {"email": "john.doe@example.com", "password": "ExamPL3P4$$W0rD!!0194"}
        }


class TokenResponseSchema(BaseModel):
    msg: str | None
    access_token: str | None
