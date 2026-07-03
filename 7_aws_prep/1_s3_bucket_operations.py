# ====================================================================
# THEORY & CONCEPT:
# Amazon S3 (Simple Storage Service) is an object storage service offering industry-leading scalability, data availability, security, and performance.
# 
# Key Architectural Elements:
# 1. Buckets: Containers for objects. Names must be globally unique across all AWS accounts.
# 2. Objects: Files and metadata. Keys represent the unique path/identifier for the object.
# 3. Consistency: Strong read-after-write consistency for PUTs and DELETEs of objects in all buckets.
# 4. Storage Classes:
#    - Standard: Frequently accessed data (high durability, low latency).
#    - Standard-IA (Infrequent Access): Less active data, lower storage price, retrieval charges.
#    - Glacier / Glacier Deep Archive: Long-term archiving, cheapest storage, retrieval takes minutes to hours.
#
# COMPLEXITY:
# - Scaling performance: S3 automatically scales to handle high request rates. You can achieve at least 3,500 PUT/COPY/POST/DELETE and 5,500 GET/HEAD requests per second per prefix.
# - Cost: Billed by GB/month, request counts (PUT/GET API calls), and data transfer out.
#
# INTERVIEW Q&A:
# Q: How do you secure data in S3?
# A: 1) Encryption: SSE-S3 (S3 managed keys), SSE-KMS (KMS managed keys), or SSE-C (Client-provided keys).
#    2) Access Control: IAM Policies, Bucket Policies, Access Control Lists (ACLs), and S3 Block Public Access.
#
# Q: What is a Pre-signed URL and why is it used?
# A: A URL generated using AWS credentials that grants temporary access to download or upload specific S3 objects. It allows clients to access secure S3 objects directly without needing AWS IAM credentials.
# ====================================================================

import os
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

class S3Service:
    def __init__(self, region_name="us-east-1"):
        """
        Initializes the boto3 S3 client.
        """
        self.s3_client = boto3.client("s3", region_name=region_name)

    def create_bucket(self, bucket_name: str, region: str = None) -> bool:
        """
        Creates an S3 bucket in a specified region.
        """
        try:
            if region is None or region == "us-east-1":
                self.s3_client.create_bucket(Bucket=bucket_name)
            else:
                location = {"LocationConstraint": region}
                self.s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration=location
                )
            print(f"Bucket '{bucket_name}' created successfully.")
            return True
        except ClientError as e:
            print(f"Failed to create bucket: {e}")
            return False

    def upload_file(self, file_path: str, bucket_name: str, object_key: str = None) -> bool:
        """
        Uploads a file to an S3 bucket.
        """
        if object_key is None:
            object_key = os.path.basename(file_path)

        try:
            self.s3_client.upload_file(file_path, bucket_name, object_key)
            print(f"File '{file_path}' successfully uploaded to '{bucket_name}/{object_key}'.")
            return True
        except FileNotFoundError:
            print(f"Local file '{file_path}' not found.")
            return False
        except (ClientError, NoCredentialsError) as e:
            print(f"Failed to upload file: {e}")
            return False

    def download_file(self, bucket_name: str, object_key: str, dest_path: str) -> bool:
        """
        Downloads a file from an S3 bucket.
        """
        try:
            self.s3_client.download_file(bucket_name, object_key, dest_path)
            print(f"Object '{object_key}' downloaded from bucket '{bucket_name}' to '{dest_path}'.")
            return True
        except (ClientError, NoCredentialsError) as e:
            print(f"Failed to download file: {e}")
            return False

    def generate_presigned_url(self, bucket_name: str, object_key: str, expiration_seconds: int = 3600) -> str:
        """
        Generates a pre-signed URL for downloading an S3 object.
        """
        try:
            url = self.s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket_name, "Key": object_key},
                ExpiresIn=expiration_seconds,
            )
            return url
        except ClientError as e:
            print(f"Failed to generate pre-signed URL: {e}")
            return None

    def list_objects(self, bucket_name: str) -> list:
        """
        Lists objects in an S3 bucket.
        """
        try:
            response = self.s3_client.list_objects_v2(Bucket=bucket_name)
            contents = response.get("Contents", [])
            object_keys = [item["Key"] for item in contents]
            return object_keys
        except ClientError as e:
            print(f"Failed to list objects in bucket '{bucket_name}': {e}")
            return []


# ====================================================================
# UNIT TEST / MOCKED RUN (Enables local execution without AWS credentials)
# ====================================================================
if __name__ == "__main__":
    import unittest
    from unittest.mock import MagicMock, patch

    class TestS3Service(unittest.TestCase):
        @patch("boto3.client")
        def test_s3_operations(self, mock_boto_client):
            # Mock the S3 client API responses
            mock_s3 = MagicMock()
            mock_boto_client.return_value = mock_s3
            
            # Setup mocks
            mock_s3.create_bucket.return_value = {"ResponseMetadata": {"HTTPStatusCode": 200}}
            mock_s3.upload_file.return_value = True
            mock_s3.download_file.return_value = True
            mock_s3.generate_presigned_url.return_value = "https://mock-s3-bucket.s3.amazonaws.com/test.txt?Signature=mock"
            mock_s3.list_objects_v2.return_value = {
                "Contents": [{"Key": "test.txt"}, {"Key": "data/sales.csv"}]
            }

            print("\n--- Running Mocked S3 Operations Test ---")
            service = S3Service(region_name="us-west-2")

            # 1. Create Bucket
            bucket = "my-test-interview-bucket"
            success = service.create_bucket(bucket, region="us-west-2")
            self.assertTrue(success)

            # 2. Upload file
            success = service.upload_file("dummy_local.txt", bucket, "test.txt")
            self.assertTrue(success)

            # 3. List objects
            objects = service.list_objects(bucket)
            print("Listed S3 objects:", objects)
            self.assertIn("test.txt", objects)

            # 4. Generate Pre-signed URL
            url = service.generate_presigned_url(bucket, "test.txt", expiration_seconds=600)
            print("Generated Pre-signed URL:", url)
            self.assertIsNotNone(url)

            # 5. Download file
            success = service.download_file(bucket, "test.txt", "downloaded_local.txt")
            self.assertTrue(success)
            print("--- S3 Mock Test Passed Successfully ---\n")

    # Run the tests
    unittest.main(argv=[''], exit=False)
