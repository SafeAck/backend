"""
OFFAT Scan views
"""

from typing import Annotated
from fastapi import APIRouter, Body, Depends, Security, Query
from sqlalchemy.orm import Session
from .schemas import ScanResultSchema
from .crud import create_result, get_user_results
from ..auth import validate_user_perms, MePerm
from ..auth.crud import get_user
from ..database import get_db
from ..logger import create_logger
from ..utils.schemas import ResponseSchema
from ..utils.db_result_handler import orm_query_response_to_dict


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


@scan_router.get("/results")
async def get_results(
    user_id: Annotated[int, Security(validate_user_perms, scopes=[MePerm.READ_RESULTS.name])],
    skip: int = Query(0, alias="page", ge=0),
    limit: int = Query(10, ge=0, le=50),
    db: Session = Depends(get_db),
):
    """allow user to view it's results"""
    msg = "failed to get scan results"
    data = None
    status_code = 500

    user = get_user(db, user_id)

    if user and user.is_active:
        status_code = 200
        msg = "scan results fetched successfully"
        scan_results = get_user_results(
            db=db,
            user_id=user_id,
            skip=skip,
            limit=limit,
        )
        data = orm_query_response_to_dict(
            query=scan_results,
            approach_type='whitelist',
        )
    else:
        status_code = 403
        msg = "user is inactive"

    return ResponseSchema(msg=msg, data=data, status_code=status_code)
