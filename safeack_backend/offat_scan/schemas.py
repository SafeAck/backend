from pydantic import BaseModel, Field, field_validator
from fastapi import HTTPException
from ..utils.regex import regexs


class ScanResultSchema(BaseModel):
    """Scan Result Post Model"""

    # example: s3://test/safeack-results/03ac6cafbea141e185570985c6316ad3.json
    s3_bucket_path: str = Field(..., min_length=10, max_length=150)

    @field_validator("s3_bucket_path")
    def validate_s3_bucket_path(cls, value: str) -> str:
        """validates s3 bucket file obj path"""
        if not regexs["s3_result_path"].match(value):
            raise HTTPException(
                status_code=400,
                detail="Invalid s3 bucket path",
            )

        return value

    class Config:
        json_schema_extra = {
            "example": {
                "s3_bucket_path": "s3://test/safeack-results/03ac6cafbea141e185570985c6316ad3.json"
            }
        }
