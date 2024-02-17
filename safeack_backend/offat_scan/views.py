"""
OFFAT Scan views
"""

from typing import Annotated
from fastapi import APIRouter, Body, Depends, Security
from sqlalchemy.orm import Session
from .schemas import ScanResultSchema
from .crud import create_result
from ..auth import validate_user_perms, MePerm
from ..auth.crud import get_user
from ..database import get_db
from ..logger import create_logger
from ..utils.schemas import ResponseSchema


logger = create_logger(__name__)

scan_router = APIRouter(prefix="/api/v1/scanner", tags=["scan"], redirect_slashes=False)


@scan_router.post("/results")
async def save_result(
    user_id: Annotated[int, Security(validate_user_perms, scopes=[MePerm.WRITE_RESULTS.name])],
    result: ScanResultSchema = Body(...),
    db: Session = Depends(get_db),
):
    """view to save result s3 bucket path"""
    msg = "failed to store scan results"
    status_code = 500
    user = get_user(db, user_id)
    if user and user.is_active:
        scan_result = create_result(db, user_id, result)
        if scan_result:
            status_code = 200
            msg = "scan results stored successfully"
    else:
        status_code = 403
        msg = "user is inactive"

    return ResponseSchema(msg=msg, data=None, status_code=status_code)
