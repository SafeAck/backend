"""
OFFAT scan models
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from ..database import Base


class ScanResult(Base):
    """Scan Result model"""

    __tablename__ = "scan_results"

    id = Column(Integer, primary_key=True)
    s3_bucket_path = Column(String(255), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
