# ====================================================================
# THEORY & CONCEPT:
# AWS IAM (Identity and Access Management) controls access authorization and authentication.
#
# Key Concepts:
# 1. Users & Groups: Permanent credentials assigned to a person or application. Groups allow collection of users.
# 2. Roles: Temporary security credentials. Principals (users, services, federated accounts) assume roles dynamically.
# 3. STS (Security Token Service): Generates temporary security credentials (Access Key ID, Secret Access Key, Session Token) when a role is assumed.
# 4. IAM Policies: JSON documents defining permissions.
#    - Identity-based Policies: Attached to users, groups, or roles.
#    - Resource-based Policies: Attached to resources (e.g., S3 buckets, SQS queues).
# 5. Principle of Least Privilege: Assigning only the minimum permissions necessary for a resource or identity to complete its task.
#
# IAM Policy Evaluation Logic:
# 1. Deny by default: All requests are denied.
# 2. Explicit Deny: If any policy contains a Deny matching the request, the final decision is Deny.
# 3. Explicit Allow: If there is an Allow and NO Deny, the final decision is Allow.
# ====================================================================

import json
import boto3
from botocore.exceptions import ClientError

class IAMService:
    def __init__(self, region_name="us-east-1"):
        self.iam = boto3.client("iam", region_name=region_name)
        self.sts = boto3.client("sts", region_name=region_name)

    def create_custom_policy(self, policy_name: str, bucket_name: str) -> str:
        """
        Creates a custom IAM policy allowing read-only access to a specific S3 bucket.
        """
        policy_document = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "s3:GetObject",
                        "s3:ListBucket"
                    ],
                    "Resource": [
                        f"arn:aws:s3:::{bucket_name}",
                        f"arn:aws:s3:::{bucket_name}/*"
                    ]
                }
            ]
        }
        
        try:
            response = self.iam.create_policy(
                PolicyName=policy_name,
                PolicyDocument=json.dumps(policy_document),
                Description=f"Read-only policy for {bucket_name} bucket."
            )
            policy_arn = response["Policy"]["Arn"]
            print(f"IAM Policy created successfully. ARN: {policy_arn}")
            return policy_arn
        except ClientError as e:
            print(f"Failed to create IAM policy: {e}")
            return None

    def create_lambda_execution_role(self, role_name: str) -> str:
        """
        Creates an IAM Role that can be assumed by AWS Lambda.
        """
        assume_role_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "lambda.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }

        try:
            response = self.iam.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps(assume_role_policy),
                Description="IAM Role allowing AWS Lambda service to assume it."
            )
            role_arn = response["Role"]["Arn"]
            print(f"IAM Role '{role_name}' created successfully. ARN: {role_arn}")
            return role_arn
        except ClientError as e:
            print(f"Failed to create IAM role: {e}")
            return None

    def attach_policy_to_role(self, role_name: str, policy_arn: str) -> bool:
        """
        Attaches a policy (by ARN) to an existing IAM role.
        """
        try:
            self.iam.attach_role_policy(
                RoleName=role_name,
                PolicyArn=policy_arn
            )
            print(f"Policy '{policy_arn}' successfully attached to role '{role_name}'.")
            return True
        except ClientError as e:
            print(f"Failed to attach policy to role: {e}")
            return False

    def assume_target_role(self, role_arn: str, session_name: str) -> dict:
        """
        Assumes another IAM role using AWS STS. Returns temporary credentials.
        These credentials can be used to initialize a new boto3 session.
        """
        try:
            response = self.sts.assume_role(
                RoleArn=role_arn,
                RoleSessionName=session_name,
                DurationSeconds=3600 # 1 hour session duration
            )
            credentials = response["Credentials"]
            print(f"Successfully assumed role '{role_arn}'. Valid until: {credentials['Expiration']}")
            return {
                "aws_access_key_id": credentials["AccessKeyId"],
                "aws_secret_access_key": credentials["SecretAccessKey"],
                "aws_session_token": credentials["SessionToken"]
            }
        except ClientError as e:
            print(f"Failed to assume role: {e}")
            return None


# ====================================================================
# UNIT TEST / MOCKED RUN (Enables local execution without AWS credentials)
# ====================================================================
if __name__ == "__main__":
    import unittest
    from unittest.mock import MagicMock, patch

    class TestIAMService(unittest.TestCase):
        @patch("boto3.client")
        def test_iam_flow(self, mock_boto_client):
            # Setup mock clients for IAM and STS
            mock_iam = MagicMock()
            mock_sts = MagicMock()

            def client_side_effect(service_name, **kwargs):
                if service_name == "iam":
                    return mock_iam
                elif service_name == "sts":
                    return mock_sts
                return MagicMock()

            mock_boto_client.side_effect = client_side_effect

            # Mock responses
            mock_iam.create_policy.return_value = {
                "Policy": {"Arn": "arn:aws:iam::123456789012:policy/TestS3ReadPolicy"}
            }
            mock_iam.create_role.return_value = {
                "Role": {"Arn": "arn:aws:iam::123456789012:role/TestLambdaRole"}
            }
            mock_iam.attach_role_policy.return_value = {}
            mock_sts.assume_role.return_value = {
                "Credentials": {
                    "AccessKeyId": "ASIAXXXXXX",
                    "SecretAccessKey": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
                    "SessionToken": "AQoDYXdzEEcaD...",
                    "Expiration": "2026-07-02T12:00:00Z"
                }
            }

            print("\n--- Running Mocked IAM & STS Operations Test ---")
            service = IAMService(region_name="us-east-1")

            # 1. Create policy
            policy_arn = service.create_custom_policy("TestS3ReadPolicy", "my-app-assets")
            self.assertEqual(policy_arn, "arn:aws:iam::123456789012:policy/TestS3ReadPolicy")

            # 2. Create role
            role_arn = service.create_lambda_execution_role("TestLambdaRole")
            self.assertEqual(role_arn, "arn:aws:iam::123456789012:role/TestLambdaRole")

            # 3. Attach policy
            success = service.attach_policy_to_role("TestLambdaRole", policy_arn)
            self.assertTrue(success)

            # 4. Assume role (Get dynamic credentials)
            temp_creds = service.assume_target_role(role_arn, "TestSession")
            self.assertIsNotNone(temp_creds)
            self.assertEqual(temp_creds["aws_access_key_id"], "ASIAXXXXXX")
            print("Acquired Temporary Session Access Key:", temp_creds["aws_access_key_id"])
            
            # Using temporary credentials to create a new session client:
            # s3_temp_client = boto3.client("s3", **temp_creds)
            
            print("--- IAM/STS Mock Test Passed Successfully ---\n")

    # Run the tests
    unittest.main(argv=[''], exit=False)
