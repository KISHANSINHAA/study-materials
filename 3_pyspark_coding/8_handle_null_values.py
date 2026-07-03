# ====================================================================
# THEORY & CONCEPT:
# PySpark DataFrame execution. Demonstrates distributed data processing, query plans, and executor-side configurations.
#
# COMPLEXITY:
# Time/Network Complexity: Shuffling determines execution bottlenecks.
# Space Complexity: Distributed executor memory layout.
#
# INTERVIEW Q&A:
# Q: What is the Spark Driver?
# A: The central coordinator that runs the main() program, creates the SparkContext/SparkSession, and schedules tasks on executors.
#
# Q: What is the difference between cache() and persist()?
# A: cache() saves data to default MEMORY_AND_DISK level. persist() allows you to customize the storage levels (e.g. MEMORY_ONLY, DISK_ONLY).
# ====================================================================

# PySpark program to handle Null/Missing values
# Demonstrates fillna() and dropna() operations.

import os
import sys
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("HandleNullValues").master("local[*]").getOrCreate()

data = [("Alice", 25, None), ("Bob", None, "Sales"), (None, 35, "HR"), ("Charlie", 40, "IT")]
df = spark.createDataFrame(data, ["Name", "Age", "Department"])

print("Original DataFrame:")
df.show()

# 1. Fill nulls: Fill null Name with 'Unknown', Age with 0, Department with 'N/A'
filled_df = df.fillna({"Name": "Unknown", "Age": 0, "Department": "N/A"})
print("Filled Nulls:")
filled_df.show()

# 2. Drop nulls: Drop rows where 'Name' or 'Age' is null
dropped_df = df.dropna(subset=["Name", "Age"])
print("Dropped Nulls:")
dropped_df.show()
