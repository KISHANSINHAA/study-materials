# ====================================================================
# THEORY & CONCEPT:
# AWS messaging services enable decoupling and horizontal scaling of microservices.
#
# Amazon SNS (Simple Notification Service):
# - Pattern: Pub/Sub (Publish/Subscribe).
# - Delivery: Push-based (sends messages directly to subscribers like Lambda, SQS, HTTP endpoints, email).
# - Use Case: Broadcast events to multiple downstream services simultaneously (Fan-out pattern).
#
# Amazon SQS (Simple Queue Service):
# - Pattern: Message Queue.
# - Delivery: Pull-based (consumers poll/retrieve messages from the queue).
# - Types of Queues:
#   1. Standard Queue: Unlimited throughput, at-least-once delivery (duplicates possible), best-effort ordering.
#   2. FIFO Queue (First-In-First-Out): Exactly-once processing, strict ordering. Limited to 300 API calls/sec (or 3000 with batching).
#
# Key SQS Settings:
# - Visibility Timeout: Time SQS prevents other consumers from receiving a message after a consumer pulls it. (Default: 30s).
# - Long Polling: Wait up to 20s for messages to arrive in the queue. Saves costs by reducing empty response API counts.
# - DLQ (Dead Letter Queue): SQS queue where failed/poison-pill messages are sent after a certain number of failed retries.
#
# COMPLEXITY:
# - Message Size: Max 256 KB.
# - Retention: 1 minute to 14 days (default 4 days).
# ====================================================================

import boto3
from botocore.exceptions import ClientError

class MessagingService:
    def __init__(self, region_name="us-east-1"):
        self.sns = boto3.client("sns", region_name=region_name)
        self.sqs = boto3.client("sqs", region_name=region_name)

    def create_topic(self, topic_name: str) -> str:
        """
        Creates an SNS Topic.
        """
        try:
            response = self.sns.create_topic(Name=topic_name)
            topic_arn = response.get("TopicArn")
            print(f"SNS Topic created: {topic_arn}")
            return topic_arn
        except ClientError as e:
            print(f"Error creating SNS topic: {e}")
            return None

    def create_queue(self, queue_name: str, is_fifo: bool = False) -> str:
        """
        Creates an SQS Queue.
        """
        attributes = {}
        if is_fifo:
            if not queue_name.endswith(".fifo"):
                queue_name += ".fifo"
            attributes = {
                "FifoQueue": "true",
                "ContentBasedDeduplication": "true"
            }
        
        try:
            response = self.sqs.create_queue(
                QueueName=queue_name,
                Attributes=attributes
            )
            queue_url = response.get("QueueUrl")
            print(f"SQS Queue created: {queue_url}")
            return queue_url
        except ClientError as e:
            print(f"Error creating SQS queue: {e}")
            return None

    def subscribe_queue_to_topic(self, topic_arn: str, queue_url: str) -> str:
        """
        Subscribes an SQS queue to an SNS topic.
        First, it queries SQS to get the Queue ARN.
        """
        try:
            # 1. Get queue ARN
            attrs = self.sqs.get_queue_attributes(
                QueueUrl=queue_url,
                AttributeNames=["QueueArn"]
            )
            queue_arn = attrs["Attributes"]["QueueArn"]

            # 2. Subscribe queue to SNS topic
            response = self.sns.subscribe(
                TopicArn=topic_arn,
                Protocol="sqs",
                Endpoint=queue_arn
            )
            subscription_arn = response.get("SubscriptionArn")
            print(f"Subscribed SQS ({queue_arn}) to SNS Topic ({topic_arn}). SubArn: {subscription_arn}")
            return subscription_arn
        except ClientError as e:
            print(f"Error subscribing SQS queue: {e}")
            return None

    def publish_to_topic(self, topic_arn: str, message: str, subject: str = None) -> str:
        """
        Publishes a message to an SNS topic.
        """
        try:
            params = {
                "TopicArn": topic_arn,
                "Message": message
            }
            if subject:
                params["Subject"] = subject
            response = self.sns.publish(**params)
            msg_id = response.get("MessageId")
            print(f"Published message {msg_id} to SNS topic.")
            return msg_id
        except ClientError as e:
            print(f"Error publishing to SNS: {e}")
            return None

    def send_sqs_message(self, queue_url: str, message_body: str) -> str:
        """
        Sends a message directly to an SQS Queue.
        """
        try:
            response = self.sqs.send_message(
                QueueUrl=queue_url,
                MessageBody=message_body
            )
            msg_id = response.get("MessageId")
            print(f"Sent message {msg_id} directly to SQS.")
            return msg_id
        except ClientError as e:
            print(f"Error sending SQS message: {e}")
            return None

    def receive_and_delete_messages(self, queue_url: str, max_messages: int = 5) -> list:
        """
        Receives messages from SQS (using long polling) and deletes them after reading.
        """
        try:
            # Receive messages using Long Polling (WaitTimeSeconds=20)
            response = self.sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=max_messages,
                WaitTimeSeconds=10, # Wait up to 10s for message
                VisibilityTimeout=30 # Hide from others for 30s
            )

            messages = response.get("Messages", [])
            processed_messages = []
            
            for msg in messages:
                body = msg["Body"]
                receipt_handle = msg["ReceiptHandle"]
                msg_id = msg["MessageId"]
                print(f"Processing message: {body} (ID: {msg_id})")
                
                # Delete message from queue so it is not processed again
                self.sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=receipt_handle
                )
                print(f"Deleted SQS message: {msg_id}")
                processed_messages.append(body)

            return processed_messages
        except ClientError as e:
            print(f"Error retrieving SQS messages: {e}")
            return []


# ====================================================================
# UNIT TEST / MOCKED RUN (Enables local execution without AWS credentials)
# ====================================================================
if __name__ == "__main__":
    import unittest
    from unittest.mock import MagicMock, patch

    class TestMessagingService(unittest.TestCase):
        @patch("boto3.client")
        def test_messaging_flow(self, mock_boto_client):
            # Setup mocks for SNS and SQS clients
            mock_sns = MagicMock()
            mock_sqs = MagicMock()

            def client_side_effect(service_name, **kwargs):
                if service_name == "sns":
                    return mock_sns
                elif service_name == "sqs":
                    return mock_sqs
                return MagicMock()

            mock_boto_client.side_effect = client_side_effect

            # Setup responses
            mock_sns.create_topic.return_value = {"TopicArn": "arn:aws:sns:us-east-1:123456789012:MyTopic"}
            mock_sqs.create_queue.return_value = {"QueueUrl": "https://queue.amazonaws.com/123456789012/MyQueue"}
            mock_sqs.get_queue_attributes.return_value = {
                "Attributes": {"QueueArn": "arn:aws:sqs:us-east-1:123456789012:MyQueue"}
            }
            mock_sns.subscribe.return_value = {"SubscriptionArn": "arn:aws:sns:us-east-1:123456789012:MyTopic:sub-id"}
            mock_sns.publish.return_value = {"MessageId": "sns-msg-123"}
            mock_sqs.send_message.return_value = {"MessageId": "sqs-msg-456"}
            
            # SQS polling returns message
            mock_sqs.receive_message.return_value = {
                "Messages": [
                    {
                        "MessageId": "sqs-msg-456",
                        "ReceiptHandle": "receipt-xxx",
                        "Body": "{\"message\": \"Hello from SNS Fan-out!\"}"
                    }
                ]
            }

            print("\n--- Running Mocked SNS & SQS Operations Test ---")
            service = MessagingService(region_name="us-east-1")

            # 1. Create SNS Topic
            topic_arn = service.create_topic("MyTopic")
            self.assertEqual(topic_arn, "arn:aws:sns:us-east-1:123456789012:MyTopic")

            # 2. Create SQS Queue
            queue_url = service.create_queue("MyQueue")
            self.assertEqual(queue_url, "https://queue.amazonaws.com/123456789012/MyQueue")

            # 3. Subscribe SQS to SNS Topic
            sub_arn = service.subscribe_queue_to_topic(topic_arn, queue_url)
            self.assertIsNotNone(sub_arn)

            # 4. Publish SNS Message
            msg_id_sns = service.publish_to_topic(topic_arn, "Hello world fan-out", "Test Subject")
            self.assertEqual(msg_id_sns, "sns-msg-123")

            # 5. Send SQS Direct message
            msg_id_sqs = service.send_sqs_message(queue_url, "Direct task enqueue")
            self.assertEqual(msg_id_sqs, "sqs-msg-456")

            # 6. Read and delete message (Polling simulation)
            messages = service.receive_and_delete_messages(queue_url)
            self.assertEqual(len(messages), 1)
            print("Successfully processed message body:", messages[0])
            print("--- SNS/SQS Mock Test Passed Successfully ---\n")

    # Run the tests
    unittest.main(argv=[''], exit=False)
