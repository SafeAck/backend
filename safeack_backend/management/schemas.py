"""
Management View Schemas
"""

from pydantic import BaseModel, Field
from ..auth.permissions import Role


class EnableUserSchema(BaseModel):
    """Enables User"""

    user_id: int = Field(..., gt=0)

    class Config:
        """enable user schema config"""

        json_schema_extra = {"example": {"user_id": 10}}


class UserSchema(BaseModel):
    """
    User Schema model
    """

    id: int = Field(
        ...,
    )
    email: str = Field(
        ...,
    )
    first_name: str = Field(
        ...,
    )
    last_name: str = Field(
        ...,
    )
    full_name: str = Field(
        ...,
    )
    is_active: bool = Field(
        ...,
    )
    is_superuser: bool = Field(
        ...,
    )
    role: Role = Field(
        ...,
    )

    class Config:
        """user details schema"""

        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "admin@example.com",
                "first_name": "Admin",
                "last_name": "User",
                "full_name": "Admin User",
                "is_active": True,
                "is_superuser": True,
                "role": "superuser",
            }
        }
