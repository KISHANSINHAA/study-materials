# ====================================================================
# THEORY & CONCEPT:
# Amazon DynamoDB is a fully managed, serverless, single-digit millisecond latency NoSQL database.
# 
# Key Concepts:
# 1. Primary Key:
#    - Simple Primary Key: Partition Key (Hash Key) only. DynamoDB uses an internal hash function to distribute items across physical partitions.
#    - Composite Primary Key: Partition Key (Hash Key) + Sort Key (Range Key). Items with the same Partition Key are sorted by the Sort Key.
# 2. Indexes:
#    - Local Secondary Index (LSI): Uses the same partition key as the table, but a different sort key. Must be created at table creation. Shares throughput with the parent table.
#    - Global Secondary Index (GSI): Can have a different partition key and sort key. Can be created/deleted at any time. Has its own allocated throughput.
# 3. Read Consistency:
#    - Eventually Consistent Reads (Default): May not reflect the results of a recently completed write. Max double throughput (2 reads per RCU).
#    - Strongly Consistent Reads: Returns a response with the most up-to-date data. Consumes 1 RCU per read.
#
# COMPLEXITY:
# - Query: O(1) or O(log N) lookup. Highly efficient as it operates only on specific partition key partitions.
# - Scan: O(N) lookup. Reads every item in the table. Extremely slow, expensive, and should be avoided in production.
#
# INTERVIEW Q&A:
# Q: How do you handle pagination in DynamoDB?
# A: DynamoDB API calls return a `LastEvaluatedKey` if the result set exceeds 1MB. To get the next page, you pass this key as the `ExclusiveStartKey` in the subsequent request.
#
# Q: What is a Hot Partition and how do you avoid it?
# A: A hot partition occurs when a single partition receives disproportionately high traffic, exceeding partition limits (3000 RCUs or 1000 WCUs). Avoid this by choosing a Partition Key with high cardinality (e.g., UUID, UserID rather than Status or Country).
# ====================================================================

import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr

class DynamoDBService:
    def __init__(self, region_name="us-east-1"):
        """
        Initializes the boto3 DynamoDB resource.
        """
        self.dynamodb = boto3.resource("dynamodb", region_name=region_name)

    def create_users_table(self, table_name: str) -> bool:
        """
        Creates a DynamoDB table with a composite key (user_id as partition key, email as sort key).
        """
        try:
            table = self.dynamodb.create_table(
                TableName=table_name,
                KeySchema=[
                    {"AttributeName": "user_id", "KeyType": "HASH"},   # Partition key
                    {"AttributeName": "email", "KeyType": "RANGE"}    # Sort key
                ],
                AttributeDefinitions=[
                    {"AttributeName": "user_id", "AttributeType": "S"},
                    {"AttributeName": "email", "AttributeType": "S"}
                ],
                ProvisionedThroughput={
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5
                }
            )
            table.wait_until_exists()
            print(f"Table '{table_name}' created successfully.")
            return True
        except ClientError as e:
            print(f"Failed to create table: {e}")
            return False

    def put_user(self, table_name: str, user_id: str, email: str, name: str, age: int, status: str) -> bool:
        """
        Inserts or overwrites an item in the DynamoDB table.
        """
        try:
            table = self.dynamodb.Table(table_name)
            table.put_item(
                Item={
                    "user_id": user_id,
                    "email": email,
                    "name": name,
                    "age": age,
                    "status": status
                }
            )
            print(f"User '{user_id}' inserted/updated successfully.")
            return True
        except ClientError as e:
            print(f"Error putting item: {e}")
            return False

    def get_user(self, table_name: str, user_id: str, email: str) -> dict:
        """
        Retrieves a single item based on the full Primary Key (Partition Key + Sort Key).
        """
        try:
            table = self.dynamodb.Table(table_name)
            response = table.get_item(
                Key={
                    "user_id": user_id,
                    "email": email
                }
            )
            return response.get("Item", None)
        except ClientError as e:
            print(f"Error getting item: {e}")
            return None

    def query_users_by_id(self, table_name: str, user_id: str) -> list:
        """
        Queries the table. Returns all items sharing the partition key (user_id).
        """
        try:
            table = self.dynamodb.Table(table_name)
            response = table.query(
                KeyConditionExpression=Key("user_id").eq(user_id)
            )
            return response.get("Items", [])
        except ClientError as e:
            print(f"Error querying table: {e}")
            return []

    def scan_active_users(self, table_name: str, status_value: str) -> list:
        """
        Scans the database. Performance warning: Scans should be minimized.
        """
        try:
            table = self.dynamodb.Table(table_name)
            response = table.scan(
                FilterExpression=Attr("status").eq(status_value)
            )
            return response.get("Items", [])
        except ClientError as e:
            print(f"Error scanning table: {e}")
            return []

    def delete_user(self, table_name: str, user_id: str, email: str) -> bool:
        """
        Deletes a user from the table.
        """
        try:
            table = self.dynamodb.Table(table_name)
            table.delete_item(
                Key={
                    "user_id": user_id,
                    "email": email
                }
            )
            print(f"User '{user_id}' deleted successfully.")
            return True
        except ClientError as e:
            print(f"Error deleting item: {e}")
            return False


# ====================================================================
# UNIT TEST / MOCKED RUN (Enables local execution without AWS credentials)
# ====================================================================
if __name__ == "__main__":
    import unittest
    from unittest.mock import MagicMock, patch

    class TestDynamoDBService(unittest.TestCase):
        @patch("boto3.resource")
        def test_dynamodb_operations(self, mock_boto_resource):
            # Mock the DynamoDB resource
            mock_db = MagicMock()
            mock_boto_resource.return_value = mock_db
            
            mock_table = MagicMock()
            mock_db.Table.return_value = mock_table
            mock_db.create_table.return_value = mock_table
            
            # Setup mocked behavior
            mock_table.get_item.return_value = {
                "Item": {
                    "user_id": "usr_100",
                    "email": "alice@example.com",
                    "name": "Alice Smith",
                    "age": 30,
                    "status": "ACTIVE"
                }
            }
            mock_table.query.return_value = {
                "Items": [
                    {"user_id": "usr_100", "email": "alice@example.com", "name": "Alice Smith"}
                ]
            }
            mock_table.scan.return_value = {
                "Items": [
                    {"user_id": "usr_100", "email": "alice@example.com", "status": "ACTIVE"},
                    {"user_id": "usr_101", "email": "bob@example.com", "status": "ACTIVE"}
                ]
            }

            print("\n--- Running Mocked DynamoDB Operations Test ---")
            service = DynamoDBService(region_name="us-east-1")
            table_name = "Users"

            # 1. Create table
            self.assertTrue(service.create_users_table(table_name))

            # 2. Put user
            self.assertTrue(service.put_user(table_name, "usr_100", "alice@example.com", "Alice Smith", 30, "ACTIVE"))

            # 3. Get user
            user = service.get_user(table_name, "usr_100", "alice@example.com")
            print("Retrieved User Profile:", user)
            self.assertIsNotNone(user)
            self.assertEqual(user["name"], "Alice Smith")

            # 4. Query user
            queried = service.query_users_by_id(table_name, "usr_100")
            print("Queried Users List:", queried)
            self.assertEqual(len(queried), 1)

            # 5. Scan active users
            active_users = service.scan_active_users(table_name, "ACTIVE")
            print("Scanned Active Users:", active_users)
            self.assertEqual(len(active_users), 2)

            # 6. Delete user
            self.assertTrue(service.delete_user(table_name, "usr_100", "alice@example.com"))
            print("--- DynamoDB Mock Test Passed Successfully ---\n")

    # Run the tests
    unittest.main(argv=[''], exit=False)
