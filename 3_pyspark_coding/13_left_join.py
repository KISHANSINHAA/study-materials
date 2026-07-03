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

# PySpark program for Left Outer Join

import os
import sys
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("LeftJoin").master("local[*]").getOrCreate()

emp_data = [(1, "Alice", 10), (2, "Bob", 20), (3, "Charlie", 99)]
emp_df = spark.createDataFrame(emp_data, ["emp_id", "name", "dept_id"])

dept_data = [(10, "HR"), (20, "IT")]
dept_df = spark.createDataFrame(dept_data, ["dept_id", "dept_name"])

# Left Join
left_joined = emp_df.join(dept_df, on="dept_id", how="left")
left_joined.show()
