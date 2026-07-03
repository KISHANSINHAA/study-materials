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

# PySpark Dense Rank Window Function

import os
import sys
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import dense_rank, col

spark = SparkSession.builder.appName("DenseRank").master("local[*]").getOrCreate()
df = spark.createDataFrame([("A", 10), ("A", 10), ("A", 20)], ["Category", "Value"])

windowSpec = Window.partitionBy("Category").orderBy(col("Value").desc())
df.withColumn("dense_rank", dense_rank().over(windowSpec)).show()
