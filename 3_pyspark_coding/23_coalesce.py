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

# PySpark Coalesce Example
# Decreases partitions. Avoids full shuffle by merging partitions on executors.

import os
import sys
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Coalesce").master("local[*]").getOrCreate()
# Spark splits small data into a few partitions
df = spark.sparkContext.parallelize(range(100), 10).toDF("Number")

print("Original partition count:", df.rdd.getNumPartitions())
# Coalesce to 2 partitions
coalesced_df = df.coalesce(2)
print("Partitions after coalesce:", coalesced_df.rdd.getNumPartitions())
