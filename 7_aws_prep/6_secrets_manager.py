# ====================================================================
# THEORY & CONCEPT:
# AWS Secrets Manager enables secure storage, rotation, and retrieval of credentials, API keys, and configuration.
#
# Secrets Manager vs SSM Parameter Store:
# - Secrets Manager: Explicitly built for sensitive secrets. Supports automatic rotation (via Lambda), cross-account sharing, and integrated replication. Cost is higher ($0.40/secret/month + API fee).
# - SSM Parameter Store: Suitable for config data and secrets. No built-in automatic rotation. Free for standard parameters; cheaper overall.
#
# KMS Integration & Envelope Encryption:
# Secrets are encrypted at rest using AWS KMS (Key Management Service). 
# Envelope encryption is used: data is encrypted using a unique data key, which is in turn encrypted using a KMS Key.
#
# Production Design Pattern: Caching Secrets
# Accessing Secrets Manager on every API call/Lambda invocation is bad practice. It leads to:
# 1. Throttling Errors: Hitting Secrets Manager API rate limits.
# 2. Increased Latency: API calls to Secrets Manager add ~50-200ms overhead.
# 3. High Costs: API requests cost $0.05 per 10,000 calls.
# Solution: Implement in-memory caching with a short Time-To-Live (TTL) (e.g., 5 to 15 minutes).
# ====================================================================

import json
import time
import boto3
from botocore.exceptions import ClientError

class SecretCacheManager:
    def __init__(self, region_name="us-east-1", cache_ttl_seconds=300):
        self.client = boto3.client("secretsmanager", region_name=region_name)
        self.cache_ttl = cache_ttl_seconds
        
        # Local cache storage: { secret_name: { "data": dict/str, "fetched_at": float } }
        self._cache = {}

    def create_secret(self, secret_name: str, secret_value: dict) -> bool:
        """
        Creates a new secret in Secrets Manager.
        """
        try:
            self.client.create_secret(
                Name=secret_name,
                SecretString=json.dumps(secret_value)
            )
            print(f"Secret '{secret_name}' created successfully.")
            return True
        except ClientError as e:
            print(f"Error creating secret: {e}")
            return False

    def get_secret(self, secret_name: str, force_refresh: bool = False) -> dict:
        """
        Retrieves a secret, utilizing the local cache if available and not expired.
        """
        current_time = time.time()
        
        # Check cache validity
        if not force_refresh and secret_name in self._cache:
            cache_entry = self._cache[secret_name]
            if (current_time - cache_entry["fetched_at"]) < self.cache_ttl:
                print(f"[CACHE HIT] Returning cached secret for: {secret_name}")
                return cache_entry["data"]

        print(f"[CACHE MISS] Fetching secret from Secrets Manager API: {secret_name}")
        try:
            response = self.client.get_secret_value(SecretId=secret_name)
            
            # A secret can be stored as a string or binary
            if "SecretString" in response:
                secret_str = response["SecretString"]
            else:
                # Decrypts binary secret using KMS and decodes it
                import base64
                secret_str = base64.b64decode(response["SecretBinary"]).decode("utf-8")

            # Parse JSON value
            try:
                secret_data = json.loads(secret_str)
            except ValueError:
                # Fallback if secret is plain text string, not json
                secret_data = {"value": secret_str}

            # Update local cache
            self._cache[secret_name] = {
                "data": secret_data,
                "fetched_at": current_time
            }
            return secret_data

        except ClientError as e:
            print(f"Failed to fetch secret: {e}")
            raise e


# ====================================================================
# UNIT TEST / MOCKED RUN (Enables local execution without AWS credentials)
# ====================================================================
if __name__ == "__main__":
    import unittest
    from unittest.mock import MagicMock, patch

    class TestSecretsManagerService(unittest.TestCase):
        @patch("boto3.client")
        def test_secret_caching_flow(self, mock_boto_client):
            mock_client = MagicMock()
            mock_boto_client.return_value = mock_client
            
            # Setup secret response
            mock_client.create_secret.return_value = {}
            mock_client.get_secret_value.return_value = {
                "SecretString": json.dumps({"db_user": "admin", "db_pass": "super_secret_password"})
            }

            print("\n--- Running Mocked Secrets Manager & Caching Test ---")
            # Create manager with a 5-second TTL cache for testing
            manager = SecretCacheManager(region_name="us-east-1", cache_ttl_seconds=5)
            secret_key = "production/database/credentials"

            # 1. Create secret
            success = manager.create_secret(secret_key, {"db_user": "admin", "db_pass": "super_secret_password"})
            self.assertTrue(success)

            # 2. First fetch: should trigger a cache miss (API call)
            creds_1 = manager.get_secret(secret_key)
            self.assertEqual(creds_1["db_user"], "admin")
            self.assertEqual(mock_client.get_secret_value.call_count, 1)

            # 3. Second fetch: should trigger a cache hit (No API call)
            creds_2 = manager.get_secret(secret_key)
            self.assertEqual(creds_2["db_pass"], "super_secret_password")
            # Call count remains 1 because of the cache hit
            self.assertEqual(mock_client.get_secret_value.call_count, 1)

            # 4. Wait for TTL to expire (simulate time passing)
            print("Simulating TTL expiration...")
            manager._cache[secret_key]["fetched_at"] -= 10 # subtract time to simulate expiry

            # 5. Third fetch: Cache expired, should trigger cache miss (API call)
            creds_3 = manager.get_secret(secret_key)
            self.assertEqual(creds_3["db_user"], "admin")
            # Call count increments to 2
            self.assertEqual(mock_client.get_secret_value.call_count, 2)
            
            print("--- Secrets Manager Mock Test Passed Successfully ---\n")

    # Run the tests
    unittest.main(argv=[''], exit=False)
