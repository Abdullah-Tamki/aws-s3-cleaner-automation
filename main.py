import boto3
import os
import json
import subprocess
from datetime import datetime, timezone, timedelta
from botocore.exceptions import ClientError

s3_client = boto3.client('s3')

def get_bucket_name():
    """Fetch the bucket name from Terraform output."""
    try:
        result = subprocess.run(
            ["terraform", "output", "-json"],
            capture_output=True,
            text=True,
            check=True
        )
        outputs = json.loads(result.stdout)
        return outputs["s3_bucket_name"]["value"]
    except Exception as e:
        print("Error getting bucket name from Terraform outputs:", e)
        exit(1)

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
        print("Files in bucket:")
        for obj in contents:
            print(f"- {obj['Key']} (LastModified: {obj['LastModified']})")


# We have two ways to handle cleanup of old S3 objects:
# 1. Terraform lifecycle rules (preferred for automation and reliability).
# 2. Python function `cleanup_old_files()` (implemented below for demonstration).
'''
def cleanup_old_files(bucket_name, days_old):
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days_old)
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    if 'Contents' in response:
        for obj in response['Contents']:
            last_modified = obj['LastModified']
            if last_modified < cutoff_date:
                s3_client.delete_object(Bucket=bucket_name, Key=obj['Key'])
                print(f"Deleted {obj['Key']} (last modified: {last_modified})")
    else:
        print("No files found for cleanup")
'''

if __name__ == "__main__":
    bucket = get_bucket_name()
    folder = "test_uploads"

    print(f"Using bucket from Terraform: {bucket}")
    upload_files(bucket, folder)
    list_files(bucket)
    #cleanup_old_files(bucket, 3)