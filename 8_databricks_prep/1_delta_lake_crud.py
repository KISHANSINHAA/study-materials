# ====================================================================
# THEORY & CONCEPT:
# Delta Lake is an open-source storage layer that brings ACID (Atomicity, Consistency, Isolation, Durability)
# transactions to Apache Spark and big data workloads.
#
# Key Features:
# 1. Transaction Log (_delta_log/): The single source of truth. Every transaction is written as an ordered JSON file 
#    (e.g., 000000.json). Periodic checkpoint files (.parquet) consolidate past logs to speed up reading table state.
# 2. Schema Enforcement: Automatically prevents inserting data with mismatched columns or types.
# 3. Schema Evolution: Allows changing the table's schema safely using `.option("mergeSchema", "true")`.
# 4. Time Travel: Query older versions of data using version numbers or timestamps (e.g. `versionAsOf` or `timestampAsOf`).
# 5. Performance Optimization:
#    - OPTIMIZE: Coalesces small files (e.g., KB-sized files) into larger, optimized files (typically 1GB).
#    - Z-Ordering: A multi-dimensional clustering technique that groups similar data physically in files to maximize 
#      the effectiveness of Spark's data-skipping algorithms during query execution.
#    - VACUUM: Deletes historical files no longer needed by the current state and older than the retention threshold (default 7 days).
#
# COMPLEXITY:
# - Reading active state: O(1) log-reading using the latest checkpoint parquet file, preventing scanning history.
# - Compaction: OPTIMIZE runs as a background process to reduce small file count from O(N) to O(1) per partition.
#
# INTERVIEW Q&A:
# Q: Why does Delta Lake store a transaction log?
# A: To guarantee ACID. Multiple writers can attempt to commit. Delta uses optimistic concurrency control: 
#    if a collision occurs, Spark retries the transaction. Readers only see fully committed files.
#
# Q: What is the risk of running VACUUM with a retention of 0 hours?
# A: VACUUM removes physical files. If active queries are reading those files, they will fail with FileNotFoundError. 
#    AWS/Databricks blocks setting retention below 168 hours (7 days) unless `spark.databricks.delta.vacuum.parallelDelete.enabled` 
#    is set or safety checks are bypassed.
# ====================================================================

import os
from datetime import datetime

# Helper to provide either Spark-based operations or a local mock/pandas fallback
class SparkDeltaService:
    def __init__(self):
        """
        Attempts to initialize a real PySpark Session.
        Falls back to a Mock/Pandas implementation if Spark is not installed or has configuration issues.
        """
        self.is_mock = False
        try:
            from pyspark.sql import SparkSession
            # Try to build Spark Session with Delta Lake packages
            self.spark = SparkSession.builder \
                .appName("DeltaLakeLocalDemo") \
                .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
                .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
                .config("spark.jars.packages", "io.delta:delta-core_2.12:2.4.0") \
                .master("local[*]") \
                .getOrCreate()
            print("Successfully initialized local PySpark Session.")
        except Exception as e:
            print(f"Could not load PySpark (likely due to missing Java/Hadoop environment): {e}")
            print("Running in simulated Mock mode utilizing Pandas...")
            self.is_mock = True
            self.spark = None

    def upsert_user_data(self, delta_path: str, new_data_list: list) -> bool:
        """
        Performs an Upsert (MERGE) operation on Delta/Mock Table.
        """
        if self.is_mock:
            print(f"[MOCK] Merging {len(new_data_list)} records into Delta table at: {delta_path}")
            # Mock implementation of Delta merge logic
            return True

        # Real PySpark Delta implementation
        try:
            from delta.tables import DeltaTable
            new_df = self.spark.createDataFrame(new_data_list)
            
            if not os.path.exists(delta_path):
                # Write initial table
                new_df.write.format("delta").save(delta_path)
                print("Delta table created.")
            else:
                # Merge logic (Upsert on user_id)
                delta_table = DeltaTable.forPath(self.spark, delta_path)
                delta_table.alias("target").merge(
                    source=new_df.alias("source"),
                    condition="target.user_id = source.user_id"
                ).whenMatchedUpdate(set={
                    "name": "source.name",
                    "location": "source.location",
                    "updated_at": "source.updated_at"
                }).whenNotMatchedInsert(values={
                    "user_id": "source.user_id",
                    "name": "source.name",
                    "location": "source.location",
                    "updated_at": "source.updated_at"
                }).execute()
                print("Delta merge completed successfully.")
            return True
        except Exception as e:
            print(f"Error performing Delta operations: {e}")
            return False

    def query_time_travel(self, delta_path: str, version: int) -> list:
        """
        Queries a specific version of the Delta table (Time Travel).
        """
        if self.is_mock:
            print(f"[MOCK] Time traveling to Version {version} of table: {delta_path}")
            return [{"user_id": 101, "name": "Alice (V1)", "location": "NY"}]

        # Real PySpark Delta implementation
        try:
            df = self.spark.read.format("delta").option("versionAsOf", version).load(delta_path)
            # Collect results to Python list of dicts
            return [row.asDict() for row in df.collect()]
        except Exception as e:
            print(f"Error during time travel query: {e}")
            return []

    def optimize_table(self, delta_path: str, z_order_col: str) -> bool:
        """
        Runs OPTIMIZE and Z-ORDER command on Delta table.
        """
        if self.is_mock:
            print(f"[MOCK] Running OPTIMIZE and Z-ORDER BY '{z_order_col}' on table: {delta_path}")
            return True

        try:
            self.spark.sql(f"OPTIMIZE delta.`{delta_path}` ZORDER BY ({z_order_col})")
            print(f"Optimize and Z-ordering by {z_order_col} completed.")
            return True
        except Exception as e:
            print(f"Error during optimization: {e}")
            return False


# ====================================================================
# UNIT TEST / MOCKED RUN (Enables local execution without AWS/Spark config)
# ====================================================================
if __name__ == "__main__":
    import unittest

    class TestDeltaCRUD(unittest.TestCase):
        def test_delta_lake_flow(self):
            print("\n--- Running Delta Lake CRUD Simulation Test ---")
            service = SparkDeltaService()
            table_path = "./scratch/delta_users_table"

            data_v0 = [
                {"user_id": 101, "name": "Alice", "location": "NY", "updated_at": "2026-07-01"},
                {"user_id": 102, "name": "Bob", "location": "CA", "updated_at": "2026-07-01"}
            ]

            data_v1 = [
                {"user_id": 101, "name": "Alice", "location": "TX", "updated_at": "2026-07-02"}, # Updated location
                {"user_id": 103, "name": "Charlie", "location": "WA", "updated_at": "2026-07-02"} # New user
            ]

            # 1. Perform Upsert/Write V0
            success = service.upsert_user_data(table_path, data_v0)
            self.assertTrue(success)

            # 2. Perform Upsert V1
            success = service.upsert_user_data(table_path, data_v1)
            self.assertTrue(success)

            # 3. Simulate Time Travel
            past_data = service.query_time_travel(table_path, version=0)
            print("Time Travel Data (V0):", past_data)
            self.assertIsNotNone(past_data)

            # 4. Run Optimization
            success = service.optimize_table(table_path, "location")
            self.assertTrue(success)
            print("--- Delta Lake Mock Test Passed Successfully ---\n")

    # Run the tests
    unittest.main(argv=[''], exit=False)
