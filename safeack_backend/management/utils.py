"""
Management App Util functions
"""

from .schemas import UserSchema
from ..models import User


def mask_user_data(users: list[User], is_superuser: bool = False) -> list[UserSchema]:
    """returns masked user data if user is not superuser"""
    response = []
    for user in users:
        response.append(
            UserSchema(
                id=user.id,
                email=user.email if is_superuser else '*@*.*',
                first_name=user.first_name,
                last_name=user.last_name,
                full_name=user.full_name,
                is_active=user.is_active,
                is_superuser=user.is_superuser,
                role=user.role,
            )
        )

    return response
