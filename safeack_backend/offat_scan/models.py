"""
OFFAT scan models
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON, Enum, Boolean
from sqlalchemy.sql import func
from .enums import HttpMethodsEnum, SeverityEnum
from ..database import Base


class ScanResult(Base):
    """Scan Result model"""

    __tablename__ = "scan_results"

    # will be used in orm_query_response_to_dict for converting model to dict
    _dict_fields_to_show = [
        'id',
        's3_bucket_path',
        'created_at',
    ]

    id = Column(Integer, primary_key=True)
    s3_bucket_path = Column(String(255), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())


class DataLeakTypeModel(Base):
    """
    Data Leak Types
    """

    __tablename__ = "scan_data_leak_types"

    id = Column(Integer, index=True, primary_key=True)
    severity = Column(Enum(SeverityEnum), index=True, nullable=False)
    description = Column(Text, nullable=False)
    name = Column(String(255), nullable=False)


class ResultTypeModel(Base):
    """
    Result based data
    """

    __tablename__ = "scan_result_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    mitigation = Column(Text, nullable=False)
    resources = Column(Text, nullable=False)
    passed_text = Column(Text, nullable=False)
    failed_text = Column(Text, nullable=False)


class ScanTestResultModel(Base):
    """
    Tests results
    """

    __tablename__ = "scan_test_results"

    # result details
    id = Column(Integer, primary_key=True, index=True)
    result_type = Column(Integer, ForeignKey("scan_result_types.id"), nullable=False)
    scan_id = Column(Integer, ForeignKey("scan_results.id"), nullable=False)
    error = Column(Boolean, nullable=False, default=False)
    data_leak_type = Column(Integer, ForeignKey("scan_data_leak_types.id"), nullable=True)

    # common request data
    method = Column(Enum(HttpMethodsEnum), nullable=False, index=True)
    endpoint = Column(String(255), nullable=False, index=True)
    url = Column(String(255), nullable=False)
    request_headers = Column(JSON, nullable=False)
    json_data = Column(JSON, nullable=True)
    query_params = Column(JSON, nullable=True)
    path_params = Column(JSON, nullable=True)
    response_headers = Column(JSON, nullable=False)
    response_status_code = Column(Integer, nullable=False)
