"""
Management User Views
"""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Security, Query
from sqlalchemy.orm import Session

from .schemas import EnableUserSchema, UserSchema
from .utils import mask_user_data
from ..auth import validate_user_perms, StaffPerm
from ..auth.crud import activate_user, is_user_superuser, get_users
from ..database import get_db
from ..logger import create_logger
from ..utils.schemas import ResponseSchema


logger = create_logger(__name__)

mgmt_router = APIRouter(prefix="/api/v1/mgmt", tags=["mgmt"], redirect_slashes=False)


@mgmt_router.post("/enable-user")
async def enable_user(
    user_id: Annotated[int, Security(validate_user_perms, scopes=[StaffPerm.ENABLE_USER.value])],
    body: EnableUserSchema = Body(...),
    db: Session = Depends(get_db),
) -> ResponseSchema:
    """endpoint used to enable user"""
    msg = "User enabled successfully"
    status_code = 200
    rows_updated = activate_user(db, body.user_id)
    if rows_updated != 1:
        msg = "Failed to enable user"
        logger.error("%d Rows updated while enabling user id %d", rows_updated, user_id)
        status_code = 500

    return ResponseSchema(msg=msg, data={}, status_code=status_code)


@mgmt_router.get("/users")
async def get_users_list(
    user_id: Annotated[
        int,
        Security(validate_user_perms, scopes=[StaffPerm.RESTRICTED_READ.value], use_cache=False),
    ],
    skip: int = Query(1, alias="page", ge=1),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
) -> list[UserSchema] | ResponseSchema:
    """
    Return a list of users. Masks data if user doesn't have admin perms.
    """
    _, is_superuser = is_user_superuser(db, user_id)
    users = get_users(db=db, skip=skip, limit=limit)
    return mask_user_data(users=users, is_superuser=is_superuser)
