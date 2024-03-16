"""
OFFAT Scan views
"""

from typing import Annotated
from fastapi import APIRouter, Body, Depends, Security, Query
from sqlalchemy.orm import Session
from .schemas import ScanResultSchema
from .crud import create_result, get_user_results, get_scan_result_bucket_path
from ..auth import validate_user_perms, MePerm
from ..auth.crud import get_user
from ..database import get_db
from ..logger import create_logger
from ..utils.aws.s3 import generate_presigned_url
from ..utils.regex import regexs
from ..utils.schemas import ResponseSchema
from ..utils.db_result_handler import orm_query_response_to_dict


logger = create_logger(__name__)

scan_router = APIRouter(prefix="/api/v1/scanner", tags=["scan"], redirect_slashes=False)


@scan_router.post("/results")
async def save_result(
    user_id: Annotated[
        int, Security(validate_user_perms, scopes=[MePerm.WRITE_RESULTS.value], use_cache=False)
    ],
    result: ScanResultSchema = Body(...),
    db: Session = Depends(get_db),
) -> ResponseSchema:
    """view to save result s3 bucket path"""
    msg = "failed to store scan results"
    status_code = 500

    scan_result = create_result(db, user_id, result)
    if scan_result:
        status_code = 200
        msg = "scan results stored successfully"

    return ResponseSchema(msg=msg, data=None, status_code=status_code)


@scan_router.get("/results")
async def get_results(
    user_id: Annotated[
        int, Security(validate_user_perms, scopes=[MePerm.READ_RESULTS.value], use_cache=False)
    ],
    skip: int = Query(0, alias="page", ge=0),
    limit: int = Query(10, ge=0, le=50),
    db: Session = Depends(get_db),
):
    """allow user to view their uploaded results"""
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

    return ResponseSchema(msg=msg, data=data, status_code=status_code)


@scan_router.get("/result-aws-link/{result_id}")
async def get_result(
    user_id: Annotated[
        int, Security(validate_user_perms, scopes=[MePerm.READ_RESULTS.value], use_cache=False)
    ],
    result_id: int,
    expiration: int = Query(300, ge=120, le=604800),
    db: Session = Depends(get_db),
):
    """allow user to generate presigned url for uploaded aws s3 bucket scan result obj"""
    msg = "failed to get scan result"
    data = None
    status_code = 404

    # Security TODO: validate whether bucket belongs to user or not
    bucket_path = get_scan_result_bucket_path(db=db, user_id=user_id, result_id=result_id)

    if bucket_path:
        matches = regexs["extract_s3_result_path"].match(bucket_path[0])
        bucket_name = matches.group(1)
        object_key = matches.group(2)

        url = generate_presigned_url(bucket_name, object_key, expiration)

        if url:
            status_code = 200
            msg = "pre-signed url generated successfully"
            data = [{"scan_result_link": url}]
        else:
            msg = "failed to generate pre-signed url"

    else:
        logger.warning("user_id: %d tried to access result_id:%d", user_id, result_id)

    return ResponseSchema(msg=msg, data=data, status_code=status_code)


@scan_router.get("/auth-ping")
async def scanner_auth_token_validation(
    user_id: Annotated[
        int, Security(validate_user_perms, scopes=[MePerm.WRITE_RESULTS.value], use_cache=False)
    ],
):
    """View to validate scanner auth token"""
    status_code = 200
    msg = "Authentication successful"

    return ResponseSchema(msg=msg, data=None, status_code=status_code)
