import boto3
import subprocess
import os

def get_bucket_name():
    result = subprocess.run(
        ["terraform", "output", "-raw", "bucket_name"],
        cwd="./terraform",
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

bucket = get_bucket_name()

s3_client = boto3.client('s3')

def upload_files(bucket_name):
    s3_client = boto3.client('s3')
    upload_folder = 'test_uploads'

    if not os.path.exists(upload_folder):
        print(f"Folder '{upload_folder}' does not exist.")
        return

    for file_name in os.listdir(upload_folder):
        file_path = os.path.join(upload_folder, file_name)
        
        if os.path.isfile(file_path):
            try:
                s3_client.upload_file(file_path, bucket_name, file_name)
                print(f"Uploaded {file_name} to {bucket_name}")
            except Exception as e:
                print(f"Error uploading {file_name}: {e}")

def list_files(bucket_name):
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    if 'Contents' in response:
        for obj in response['Contents']:
            print(obj['Key'])
    else:
        print("No files found.")


if __name__ == "__main__":
    bucket = get_bucket_name()
    upload_files(bucket)
    list_files(bucket)