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

# PySpark program to remove duplicates from a DataFrame

import os
import sys
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("RemoveDuplicates").master("local[*]").getOrCreate()

data = [("Alice", 25), ("Bob", 30), ("Alice", 25), ("Alice", 28)]
df = spark.createDataFrame(data, ["Name", "Age"])

# Remove exact duplicate rows
dedup_all = df.dropDuplicates()
print("Deduplicated (All Columns):")
dedup_all.show()

# Remove duplicate rows based on subset of columns
dedup_subset = df.dropDuplicates(["Name"])
print("Deduplicated (Name Column Subset):")
dedup_subset.show()
