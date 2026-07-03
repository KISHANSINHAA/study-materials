# ====================================================================
# THEORY & CONCEPT:
# AWS Lambda is a serverless, event-driven compute service that lets you run code without provisioning servers.
#
# Lambda Handler Signature:
# The entry point signature is: def lambda_handler(event, context)
# - event: A JSON-formatted document containing data for the Lambda function to process. The structure depends on the trigger source.
# - context: An object containing runtime information, such as function name, limits, request ID, and remaining execution time.
#
# Execution Environment Lifecycle:
# 1. Init Phase: System spins up a container, downloads package, and runs initialization code (outside the handler).
# 2. Invoke Phase: Runs the actual handler code.
# 3. Shutdown Phase: Clean up.
#
# Cold Starts:
# The latency overhead that occurs when AWS initializes a new instance of your function to handle a request.
# - Optimization:
#   - Declare database connections, boto3 clients, and static configs OUTSIDE the handler. They remain initialized in memory for subsequent invocations (warm container reuse).
#   - Keep package sizes minimal (e.g. avoid unused libraries).
#   - Use Provisioned Concurrency if real-time low-latency response is guaranteed.
#
# COMPLEXITY:
# - Timeout: Max 15 minutes (900 seconds).
# - Memory: 128 MB to 10,240 MB. CPU scales proportionally.
# - Concurrency: Default regional account limit is 1,000.
# ====================================================================

import json
import logging
import os
import boto3

# GOOD PRACTICE: Initialize logger and boto3 clients OUTSIDE the handler for warm container reuse!
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Dummy boto3 client (e.g., S3 client) initialized here to save time on subsequent invocations
s3_client = boto3.client("s3")

def lambda_handler(event, context):
    """
    Main entry point for AWS Lambda. Handles routing based on event source.
    """
    logger.info("Received Lambda event: %s", json.dumps(event))
    
    # 1. Check if the event is triggered by API Gateway (HTTP Request)
    if "httpMethod" in event or "requestContext" in event:
        return handle_api_gateway_event(event, context)
        
    # 2. Check if the event is triggered by S3
    elif "Records" in event and event["Records"][0].get("eventSource") == "aws:s3":
        return handle_s3_event(event, context)
        
    # 3. Check if the event is triggered by SQS
    elif "Records" in event and event["Records"][0].get("eventSource") == "aws:sqs":
        return handle_sqs_event(event, context)
        
    # 4. Fallback default execution
    else:
        logger.warning("Unknown event source")
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Unsupported event source trigger."})
        }

def handle_api_gateway_event(event, context):
    """
    Processes REST/HTTP APIs via API Gateway.
    """
    logger.info("Processing API Gateway request...")
    method = event.get("httpMethod", "GET")
    query_params = event.get("queryStringParameters") or {}
    
    # Safely parse request body
    body = {}
    if event.get("body"):
        try:
            body = json.loads(event["body"])
        except ValueError:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Invalid JSON in request body."})
            }

    name = query_params.get("name") or body.get("name") or "Guest User"
    
    # Context helper checking remaining execution time
    remaining_time = context.get_remaining_time_in_millis() if hasattr(context, 'get_remaining_time_in_millis') else 0
    
    response_body = {
        "message": f"Hello {name} from AWS Lambda!",
        "aws_request_id": context.aws_request_id if hasattr(context, 'aws_request_id') else "local_test",
        "remaining_ms": remaining_time
    }

    # API Gateway expects specific output structure
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*" # Enable CORS
        },
        "body": json.dumps(response_body)
    }

def handle_s3_event(event, context):
    """
    Processes S3 Put/Delete events.
    """
    logger.info("Processing S3 Event...")
    for record in event["Records"]:
        bucket_name = record["s3"]["bucket"]["name"]
        object_key = record["s3"]["object"]["key"]
        event_name = record["eventName"]
        logger.info(f"S3 Event '{event_name}' on file '{object_key}' in bucket '{bucket_name}'")
        
        # Programmatic Boto3 operation example
        try:
            # metadata = s3_client.head_object(Bucket=bucket_name, Key=object_key)
            # logger.info(f"Metadata ContentType: {metadata['ContentType']}")
            pass
        except Exception as e:
            logger.error(f"Error fetching metadata: {e}")
            
    return {"status": "SUCCESS", "processed_records": len(event["Records"])}

def handle_sqs_event(event, context):
    """
    Processes incoming messages from SQS batch triggers.
    """
    logger.info("Processing SQS batch queue...")
    processed_count = 0
    for record in event["Records"]:
        message_id = record["messageId"]
        body_content = record["body"]
        logger.info(f"SQS Processing MsgID: {message_id} | Body: {body_content}")
        processed_count += 1
        
    return {"status": "SUCCESS", "processed_messages": processed_count}


# ====================================================================
# LOCAL TESTING SUITE (Enables local execution/simulation of Lambda events)
# ====================================================================
if __name__ == "__main__":
    import unittest
    from unittest.mock import MagicMock

    class TestLambdaHandlers(unittest.TestCase):
        def setUp(self):
            # Create a mock context object
            self.mock_context = MagicMock()
            self.mock_context.aws_request_id = "test-req-12345"
            self.mock_context.get_remaining_time_in_millis.return_value = 8500

        def test_api_gateway_trigger(self):
            print("\n--- Simulating API Gateway Lambda Trigger ---")
            api_event = {
                "httpMethod": "POST",
                "body": json.dumps({"name": "Devan Sinha"}),
                "queryStringParameters": None
            }
            res = lambda_handler(api_event, self.mock_context)
            self.assertEqual(res["statusCode"], 200)
            
            body = json.loads(res["body"])
            print("API Gateway Output Body:", body)
            self.assertIn("Devan Sinha", body["message"])

        def test_s3_trigger(self):
            print("\n--- Simulating S3 Upload Lambda Trigger ---")
            s3_event = {
                "Records": [
                    {
                        "eventSource": "aws:s3",
                        "eventName": "ObjectCreated:Put",
                        "s3": {
                            "bucket": {"name": "test-data-bucket"},
                            "object": {"key": "uploads/images/profile.png"}
                        }
                    }
                ]
            }
            res = lambda_handler(s3_event, self.mock_context)
            self.assertEqual(res["status"], "SUCCESS")
            self.assertEqual(res["processed_records"], 1)

        def test_sqs_trigger(self):
            print("\n--- Simulating SQS Queue Lambda Trigger ---")
            sqs_event = {
                "Records": [
                    {
                        "eventSource": "aws:sqs",
                        "messageId": "msg-9991",
                        "body": "Process order transaction 405"
                    }
                ]
            }
            res = lambda_handler(sqs_event, self.mock_context)
            self.assertEqual(res["status"], "SUCCESS")
            self.assertEqual(res["processed_messages"], 1)

    # Run the tests
    unittest.main(argv=[''], exit=False)
