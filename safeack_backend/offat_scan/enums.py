"""
Enums module for models
"""

from enum import Enum


class HttpMethodsEnum(Enum):
    """
    HTTP methods enum for ScanTestResultModel
    """

    GET = "GET"
    HEAD = "HEAD"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"
    CONNECT = "CONNECT"
    TRACE = "TRACE"


class SeverityEnum(Enum):
    """
    Common Attack/Data Leak Severities
    """

    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    TRIVIAL = "TRIVIAL"
