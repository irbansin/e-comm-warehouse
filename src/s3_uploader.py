import boto3
from botocore.exceptions import NoCredentialsError
from config import AWS_ACCESS_KEY, AWS_SECRET_KEY

s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)

def check_file_exists(bucket_name, file_key):
    try:
        s3_client.head_object(Bucket=bucket_name, Key=file_key)
        return True
    except Exception as e:
        return False

def upload_to_s3(file_name, bucket, object_name=None):
    """Upload a file to S3 bucket"""
    if check_file_exists(bucket, object_name or file_name):
        print(f"File {object_name or file_name} already exists in S3 bucket {bucket}. Aborting...")
        return False
    try:
        s3_client.upload_file(file_name, bucket, object_name or file_name)
        print(f"Uploaded {file_name} to S3 bucket {bucket}")
        return True
    except FileNotFoundError:
        print(f"The file {file_name} was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False
    except Exception as e:
        print(f"An error occurred while uploading to S3: {e}")
        return False
