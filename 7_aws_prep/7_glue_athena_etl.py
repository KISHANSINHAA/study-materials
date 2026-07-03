# ====================================================================
# THEORY & CONCEPT:
# Serverless Big Data & Analytics in AWS: Amazon Athena & AWS Glue.
#
# AWS Glue:
# - Glue Data Catalog: A managed, Hive-compliant metastore that stores table definitions, schemas, and partition info for S3 files.
# - Crawlers: Automatically connect to S3 source data, infer schemas, and write table metadata into the Data Catalog.
# - Glue Jobs: Serverless Apache Spark (or Python) ETL execution environment.
#
# Amazon Athena:
# - An interactive query service that enables running standard SQL queries directly on data stored in S3.
# - Engine: Based on Presto/Trino query engines.
# - Cost: Charged based on the amount of data scanned ($5.00/TB).
#
# Athena Performance & Cost Optimization:
# 1. Columnar Formats: Convert CSV/JSON to Apache Parquet or ORC. This allows Athena to query only the necessary columns instead of scanning the whole file.
# 2. Partitioning: Organize S3 data in folders like `/year=2026/month=07/`. This restricts Athena to scan only matching partitions.
# 3. Compression: Compress files (e.g., Snappy compression for Parquet) to minimize size.
# 4. File Size: Avoid the "small file problem" (millions of KB-sized files). Aim for files of 128MB to 512MB to reduce metadata scanning overhead.
# ====================================================================

import time
import boto3
from botocore.exceptions import ClientError

class AthenaService:
    def __init__(self, database: str, output_s3_bucket: str, region_name="us-east-1"):
        """
        Initializes the Athena client.
        - database: The Glue Database to query.
        - output_s3_bucket: S3 bucket location where Athena stores query results (required).
        """
        self.client = boto3.client("athena", region_name=region_name)
        self.database = database
        self.output_s3_location = f"s3://{output_s3_bucket}/athena-results/"

    def run_query_and_wait(self, query_string: str, poll_interval: int = 2, timeout: int = 60) -> str:
        """
        Submits an Athena SQL query and polls until it finishes. Returns query execution ID.
        """
        try:
            # 1. Submit the query
            response = self.client.start_query_execution(
                QueryString=query_string,
                QueryExecutionContext={"Database": self.database},
                ResultConfiguration={"OutputLocation": self.output_s3_location}
            )
            query_execution_id = response["QueryExecutionId"]
            print(f"Submitted Athena Query. Execution ID: {query_execution_id}")

            # 2. Poll query status
            start_time = time.time()
            while time.time() - start_time < timeout:
                status_resp = self.client.get_query_execution(QueryExecutionId=query_execution_id)
                state = status_resp["QueryExecution"]["Status"]["State"]
                
                if state in ["SUCCEEDED"]:
                    print(f"Query {query_execution_id} completed successfully.")
                    return query_execution_id
                elif state in ["FAILED", "CANCELLED"]:
                    reason = status_resp["QueryExecution"]["Status"].get("StateChangeReason", "Unknown error")
                    raise Exception(f"Query execution {state}. Reason: {reason}")
                
                # Wait before checking again
                time.sleep(poll_interval)
            
            raise TimeoutError("Athena query exceeded maximum timeout.")
        except ClientError as e:
            print(f"Error running Athena query: {e}")
            raise e

    def get_query_results_parsed(self, query_execution_id: str) -> list:
        """
        Retrieves the results of a succeeded query and parses them into a list of dicts.
        """
        try:
            results = self.client.get_query_results(QueryExecutionId=query_execution_id)
            rows = results["ResultSet"]["Rows"]
            
            if not rows:
                return []

            # First row contains headers
            headers = [col.get("VarCharValue", "") for col in rows[0]["Data"]]
            parsed_data = []

            for row in rows[1:]:
                row_data = {}
                for idx, col in enumerate(row["Data"]):
                    val = col.get("VarCharValue", None)
                    row_data[headers[idx]] = val
                parsed_data.append(row_data)

            return parsed_data
        except ClientError as e:
            print(f"Error fetching query results: {e}")
            return []


# ====================================================================
# SKELETON: AWS GLUE PYSPARK JOB (Conceptual production code pattern)
# ====================================================================
def sample_glue_pyspark_job_skeleton():
    """
    This function represents the exact standard template used in AWS Glue Spark Jobs.
    It is not executed locally in the unit tests but serves as code reference.
    """
    # Standard AWS Glue Boilerplate imports
    try:
        from pyspark.context import SparkContext
        from awsglue.context import GlueContext
        from awsglue.job import Job
        from awsglue.utils import getResolvedOptions
        import sys

        # Resolve system parameters passed to Glue Job
        args = getResolvedOptions(sys.argv, ['JOB_NAME'])
        
        # Initialize contexts
        sc = SparkContext()
        glueContext = GlueContext(sc)
        spark = glueContext.spark_session
        job = Job(glueContext)
        job.init(args['JOB_NAME'], args)

        # 1. Read catalog table metadata into a Glue DynamicFrame
        datasource = glueContext.create_dynamic_frame.from_catalog(
            database="sales_db",
            table_name="raw_transactions"
        )

        # 2. Convert to PySpark DataFrame to run typical transformations
        df = datasource.toDF()
        transformed_df = df.filter(df["amount"] > 100).select("transaction_id", "amount", "user_id")

        # 3. Write back to S3 in optimized Parquet format
        from awsglue.dynamicframe import DynamicFrame
        transformed_dyf = DynamicFrame.fromDF(transformed_df, glueContext, "transformed_dyf")
        
        glueContext.write_dynamic_frame.from_options(
            frame=transformed_dyf,
            connection_type="s3",
            connection_options={"path": "s3://processed-analytics-bucket/sales/"},
            format="parquet"
        )
        
        job.commit()
    except ImportError:
        # Expected locally because Glue/PySpark libs are only present in AWS Glue runtime environment.
        pass


# ====================================================================
# UNIT TEST / MOCKED RUN (Enables local execution without AWS credentials)
# ====================================================================
if __name__ == "__main__":
    import unittest
    from unittest.mock import MagicMock, patch

    class TestAthenaService(unittest.TestCase):
        @patch("boto3.client")
        def test_athena_flow(self, mock_boto_client):
            mock_client = MagicMock()
            mock_boto_client.return_value = mock_client
            
            # Setup responses
            mock_client.start_query_execution.return_value = {"QueryExecutionId": "query-id-112233"}
            
            # First status call returns RUNNING, second returns SUCCEEDED
            mock_client.get_query_execution.side_effect = [
                {"QueryExecution": {"Status": {"State": "RUNNING"}}},
                {"QueryExecution": {"Status": {"State": "SUCCEEDED"}}}
            ]

            mock_client.get_query_results.return_value = {
                "ResultSet": {
                    "Rows": [
                        {"Data": [{"VarCharValue": "user_id"}, {"VarCharValue": "total_spend"}]}, # Headers
                        {"Data": [{"VarCharValue": "usr_90"}, {"VarCharValue": "450.50"}]},      # Row 1
                        {"Data": [{"VarCharValue": "usr_91"}, {"VarCharValue": "1200.00"}]}      # Row 2
                    ]
                }
            }

            print("\n--- Running Mocked Athena Query Operations Test ---")
            service = AthenaService(database="analytics_db", output_s3_bucket="my-athena-logs-bucket")

            # 1. Run query (Should poll status twice)
            query = "SELECT user_id, SUM(amount) as total_spend FROM sales GROUP BY user_id"
            query_id = service.run_query_and_wait(query, poll_interval=1)
            self.assertEqual(query_id, "query-id-112233")
            self.assertEqual(mock_client.get_query_execution.call_count, 2)

            # 2. Get and parse results
            results = service.get_query_results_parsed(query_id)
            print("Athena Parsed Query Results:")
            for row in results:
                print("  ", row)
            
            self.assertEqual(len(results), 2)
            self.assertEqual(results[0]["user_id"], "usr_90")
            self.assertEqual(results[1]["total_spend"], "1200.00")
            print("--- Athena Mock Test Passed Successfully ---\n")

    # Run the tests
    unittest.main(argv=[''], exit=False)
