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

# PySpark Cache and Persist DataFrame
# Used to persist intermediate DataFrames in memory/disk to speed up iterative algorithms.

import os
import sys
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

from pyspark.sql import SparkSession
from pyspark import StorageLevel

spark = SparkSession.builder.appName("CachePersist").master("local[*]").getOrCreate()
df = spark.createDataFrame([("A", 1)], ["Col1", "Col2"])

# cache() uses default storage level (MEMORY_AND_DISK)
df_cached = df.cache()
# Force evaluation to cache data
df_cached.count()

# persist() allows custom storage levels (e.g., MEMORY_ONLY, DISK_ONLY, etc.)
# Note: Spark dataframe can't have both cache and persist at the same time, we must unpersist first.
df.unpersist()
df_persisted = df.persist(StorageLevel.MEMORY_AND_DISK_2) # Replicated on two nodes
df_persisted.count()

print("DataFrame is successfully cached and persisted.")
df.unpersist()
