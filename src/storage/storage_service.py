import boto3
from botocore.exceptions import ClientError
from typing import BinaryIO
from src.config import get_settings

settings = get_settings()


def _get_client():
    return boto3.client(
        "s3",
        endpoint_url=settings.storage_endpoint,
        aws_access_key_id=settings.storage_access_key,
        aws_secret_access_key=settings.storage_secret_key,
        use_ssl=settings.storage_use_ssl,
    )


def ensure_bucket_exists() -> None:
    client = _get_client()
    try:
        client.head_bucket(Bucket=settings.storage_bucket)
    except ClientError:
        client.create_bucket(Bucket=settings.storage_bucket)
        # Enable SSE-S3 (AES-256) — NFR-03
        client.put_bucket_encryption(
            Bucket=settings.storage_bucket,
            ServerSideEncryptionConfiguration={
                "Rules": [{"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}}]
            },
        )


def upload_file(file_obj: BinaryIO, storage_key: str, content_type: str = "application/octet-stream") -> str:
    client = _get_client()
    client.upload_fileobj(
        file_obj,
        settings.storage_bucket,
        storage_key,
        ExtraArgs={
            "ContentType": content_type,
            "ServerSideEncryption": "AES256",
        },
    )
    return storage_key


def download_file(storage_key: str) -> bytes:
    client = _get_client()
    response = client.get_object(Bucket=settings.storage_bucket, Key=storage_key)
    return response["Body"].read()


def generate_presigned_url(storage_key: str, expires_in: int = 3600) -> str:
    client = _get_client()
    return client.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.storage_bucket, "Key": storage_key},
        ExpiresIn=expires_in,
    )


def delete_file(storage_key: str) -> None:
    client = _get_client()
    client.delete_object(Bucket=settings.storage_bucket, Key=storage_key)
