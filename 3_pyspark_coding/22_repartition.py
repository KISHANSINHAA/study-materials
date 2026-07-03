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

# PySpark Repartition Example
# Increases or decreases partitions. Involves full shuffle.

import os
import sys
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Repartition").master("local[*]").getOrCreate()
df = spark.createDataFrame([("A", 1), ("B", 2)], ["Col1", "Col2"])

print("Default partition count:", df.rdd.getNumPartitions())
# Repartition to 4
repartitioned_df = df.repartition(4)
print("Partitions after repartition:", repartitioned_df.rdd.getNumPartitions())
