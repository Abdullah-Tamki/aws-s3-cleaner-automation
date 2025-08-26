import boto3
import os
from botocore.exceptions import ClientError
from datetime import datetime, timezone, timedelta

s3_client = boto3.client('s3')

def create_bucket(bucket_name):
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' already exists.")

    except ClientError:
        region = s3_client.meta.region_name
        if region == "us-east-1":
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        print(f"Bucket '{bucket_name}' created ssuccessfully!")

def upload_files(bucket_name, folder_path):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            s3_client.upload_file(file_path, bucket_name, file_name)
            print(f"Uploaded {file_name} to {bucket_name}")

def list_files(bucket_name):
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    contents = response.get('Contents', [])
    if not contents:
        print("No files in the bucket.")
    else:
        for obj in contents:
            print(obj['Key'])

def cleanup_old_files(bucket_name, days_old):
    cuttoff_date = datetime.now(timezone.utc) - timedelta(days=days_old)
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    if 'Contents' in response:
        for obj in response['Contents']:
            last_modified = obj['LastModified']
            if last_modified < cuttoff_date:
                s3_client.delete_object(Bucket=bucket_name, Key=obj['Key'])
                print(f"Deleted {obj['Key']} (last modified: {last_modified})")
    
    else:
        print("No files found for cleanup")


if __name__ == "__main__":
    bucket = "my-s3-cleaner-demo-bucket-2025"
    folder = "test_uploads"
    create_bucket(bucket)
    upload_files(bucket, folder)
    list_files(bucket)
    cleanup_old_files(bucket, 3)