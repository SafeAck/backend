"""
AWS S3 util functions
"""

from sys import exc_info
from boto3 import client
from botocore.exceptions import ClientError
from ...logger import create_logger

logger = create_logger(__name__)


def generate_presigned_url(
    bucket_name: str,
    object_key: str,
    expiration_time: int = 3600,
) -> str | None:
    """
    Generate a pre-signed URL for an S3 object.

    Params:
        bucket_name (str): Name of the S3 bucket.
        object_key (str): Key of the S3 object (path).
        expiration_time (int): Expiration time of the URL in seconds (default is 1 hour).

    Returns:
        str: Pre-signed URL as a string or None if error occurs.
    """
    # Create an S3 client
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#credentials
    # ask user to create bucket in specific region instead of providing multiple options
    s3_client = client('s3')

    # Generate a pre-signed URL for the S3 object
    try:
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/generate_presigned_url.html#S3.Client.generate_presigned_url
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_key},
            ExpiresIn=expiration_time,
            HttpMethod='GET',
        )
        return response
    except ClientError as e:
        logger.info("Unable to create presigned url due to error: %s", e, exc_info=exc_info)
        return None
