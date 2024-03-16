from sqlalchemy import and_
from sqlalchemy.orm import Session
from .models import ScanResult
from .schemas import ScanResultSchema


def get_user_results(db: Session, user_id: int, skip: int = 0, limit: int = 50) -> list[ScanResult]:
    """get all scans for provided user id"""
    skip = (skip - 1) * limit

    return (
        db.query(ScanResult)
        .filter(ScanResult.owner_id == user_id)
        .order_by(ScanResult.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_result(db: Session, user_id: int, result: ScanResultSchema):
    """stores scan result details into db"""
    scan_result = ScanResult(
        s3_bucket_path=result.s3_bucket_path,
        owner_id=user_id,
    )
    db.add(scan_result)
    db.commit()
    db.refresh(scan_result)
    return scan_result


def get_scan_result_bucket_path(db: Session, user_id: int, result_id: int) -> str | None:
    """get storage bucket for specific result id"""
    return (
        db.query(ScanResult.s3_bucket_path)
        .filter(and_(ScanResult.owner_id == user_id, ScanResult.id == result_id))
        .first()
    )
