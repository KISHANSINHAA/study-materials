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

# PySpark program demonstrating Window Functions
# Sets up a window specification partitioned by department and ordered by salary.

import os
import sys
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import col, row_number, rank, dense_rank

spark = SparkSession.builder.appName("WindowFunctions").master("local[*]").getOrCreate()

data = [
    ("HR", "Alice", 5000),
    ("HR", "Bob", 6000),
    ("HR", "Carol", 6000),
    ("IT", "David", 8000),
    ("IT", "Emma", 9000)
]
df = spark.createDataFrame(data, ["Department", "Name", "Salary"])

# Define Window Specification
windowSpec = Window.partitionBy("Department").orderBy(col("Salary").desc())

# Calculate Row Number, Rank, and Dense Rank
result_df = df.withColumn("row_number", row_number().over(windowSpec)) \
              .withColumn("rank", rank().over(windowSpec)) \
              .withColumn("dense_rank", dense_rank().over(windowSpec))

result_df.show()
