# ====================================================================
# THEORY & CONCEPT:
# Medallion Architecture is a data design pattern that logically organizes data in a Lakehouse. 
# The goal is to incrementally improve the structure and quality of data as it flows through layers:
#
# 1. Bronze Layer (Raw Ingestion):
#    - Stores raw data exactly as received from sources (Append-only).
#    - Keeps raw historical records, allowing data reprocessing from scratch if bugs are found later.
#    - Schema is flexible and contains unvalidated data.
# 2. Silver Layer (Cleaned & Conformed):
#    - Cleans, parses, standardizes, enriches, and deduplicates the data.
#    - Schema is strictly enforced (Delta tables).
#    - Can combine data from multiple sources (joins).
# 3. Gold Layer (Business Aggregations):
#    - Aggregated, business-ready tables modeled for specific reporting and analytical use cases.
#    - Often structured as Star Schema (Fact and Dimension tables) or pre-aggregated tables.
#    - The primary source of data for BI dashboards (e.g. Power BI, Tableau).
#
# COMPLEXITY:
# - Decoupling: Divides long, fragile ETL scripts into isolated, manageable pipelines (Bronze->Silver, Silver->Gold).
# - Retries: In case of schema failures, raw data remains preserved in Bronze, reducing data loss risk.
#
# INTERVIEW Q&A:
# Q: Can you query the Silver layer directly from a BI tool?
# A: Yes, but it is not recommended. Silver tables are often detailed transactions. Querying them directly 
#    can cause slow dashboard load times and high compute bills. Gold tables should be queried instead.
#
# Q: How do you handle schema evolution in this architecture?
# A: Raw ingestion in Bronze is schema-agnostic. In Silver, schema evolution is handled explicitly by enabling 
#    `.option("mergeSchema", "true")` during writes, ensuring schema validation catches bad records first.
# ====================================================================

import pandas as pd
from datetime import datetime, timezone

class MedallionETLPipeline:
    def __init__(self):
        # Database lists representing our Bronze, Silver, and Gold delta tables
        self.bronze_store = []
        self.silver_store = []
        self.gold_store = []

    def ingest_to_bronze(self, raw_payloads: list):
        """
        Bronze Layer: Direct ingestion of raw JSON payloads.
        No validation is performed. Data is appended with ingestion timestamps.
        """
        print(f"Bronze Ingestion: Processing {len(raw_payloads)} raw inputs...")
        for payload in raw_payloads:
            bronze_record = payload.copy()
            bronze_record["_ingestion_time"] = datetime.now(timezone.utc).isoformat()
            self.bronze_store.append(bronze_record)
        print("Bronze Store updated successfully.")

    def transform_bronze_to_silver(self) -> int:
        """
        Silver Layer: Clean, conform, drop duplicates, and parse datatypes.
        """
        print("Silver ETL: Cleaning raw Bronze data...")
        df_bronze = pd.DataFrame(self.bronze_store)
        
        if df_bronze.empty:
            return 0

        # 1. Clean data: drop rows with missing critical IDs
        df_clean = df_bronze.dropna(subset=["transaction_id"])
        
        # 2. Conform types: parse dates and numeric values
        df_clean = df_clean.copy()
        df_clean["amount"] = pd.to_numeric(df_clean["amount"], errors="coerce").fillna(0.0)
        df_clean["transaction_date"] = pd.to_datetime(df_clean["transaction_date"], errors="coerce")

        # 3. Deduplicate based on unique key (keep the latest ingestion)
        df_clean = df_clean.sort_values(by=["transaction_id", "_ingestion_time"])
        df_silver = df_clean.drop_duplicates(subset=["transaction_id"], keep="last")

        # Overwrite Silver table
        self.silver_store = df_silver.to_dict(orient="records")
        print(f"Silver Store updated with {len(self.silver_store)} clean records.")
        return len(self.silver_store)

    def aggregate_silver_to_gold(self) -> int:
        """
        Gold Layer: Aggregate data for business reporting.
        Calculate total revenue and sales count per product category.
        """
        print("Gold ETL: Aggregating data for BI dashboard reporting...")
        df_silver = pd.DataFrame(self.silver_store)

        if df_silver.empty:
            return 0

        # Group by category and compute aggregates
        df_gold = df_silver.groupby("category").agg(
            total_revenue=("amount", "sum"),
            sales_count=("transaction_id", "count")
        ).reset_index()

        df_gold["_report_generation_time"] = datetime.now(timezone.utc).isoformat()
        
        # Save to Gold storage
        self.gold_store = df_gold.to_dict(orient="records")
        print(f"Gold Store updated with {len(self.gold_store)} aggregated analytics rows.")
        return len(self.gold_store)


# ====================================================================
# UNIT TEST / VERIFICATION SUITE
# ====================================================================
if __name__ == "__main__":
    import unittest

    class TestMedallionArchitecture(unittest.TestCase):
        def test_pipeline_execution(self):
            pipeline = MedallionETLPipeline()

            # Simulated raw API payloads (duplicates and dirty fields included)
            raw_data = [
                {"transaction_id": "tx_01", "amount": "150.00", "category": "Electronics", "transaction_date": "2026-07-01"},
                {"transaction_id": "tx_02", "amount": "80.50", "category": "Books", "transaction_date": "2026-07-01"},
                {"transaction_id": "tx_01", "amount": "150.00", "category": "Electronics", "transaction_date": "2026-07-01"}, # Duplicate
                {"transaction_id": "tx_03", "amount": "invalid_num", "category": "Books", "transaction_date": "2026-07-02"},  # Dirty data
                {"transaction_id": None, "amount": "10.00", "category": "Unknown", "transaction_date": "2026-07-02"}         # Null key
            ]

            print("\n--- Executing Medallion Pipeline Test ---")
            # 1. Bronze ingestion
            pipeline.ingest_to_bronze(raw_data)
            self.assertEqual(len(pipeline.bronze_store), 5)

            # 2. Silver Transformation (should yield 3 unique records, skipping null key)
            clean_count = pipeline.transform_bronze_to_silver()
            self.assertEqual(clean_count, 3)

            # 3. Gold Aggregation
            report_count = pipeline.aggregate_silver_to_gold()
            self.assertEqual(report_count, 2) # Electronics and Books

            # Verify aggregation calculations
            gold_df = pd.DataFrame(pipeline.gold_store)
            electronics_row = gold_df[gold_df["category"] == "Electronics"].iloc[0]
            books_row = gold_df[gold_df["category"] == "Books"].iloc[0]

            self.assertEqual(electronics_row["total_revenue"], 150.00)
            self.assertEqual(books_row["total_revenue"], 80.50) # Invalid_num converted to 0.0 + 80.50 = 80.50
            self.assertEqual(books_row["sales_count"], 2)

            print("--- Medallion Architecture Test Passed Successfully ---\n")

    unittest.main(argv=[''], exit=False)
