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

# PySpark program for Full Outer Join

import os
import sys
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("FullJoin").master("local[*]").getOrCreate()

emp_df = spark.createDataFrame([(1, "Alice", 10), (2, "Bob", 99)], ["id", "name", "dept_id"])
dept_df = spark.createDataFrame([(10, "HR"), (20, "IT")], ["dept_id", "dept_name"])

full_joined = emp_df.join(dept_df, on="dept_id", how="full")
full_joined.show()
