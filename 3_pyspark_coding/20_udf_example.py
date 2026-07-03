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

# PySpark program demonstrating User Defined Functions (UDFs)
# Custom string conversion logic registered and applied on DataFrame.

import os
import sys
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

spark = SparkSession.builder.appName("UDFExample").master("local[*]").getOrCreate()

data = [("alice",), ("bob",)]
df = spark.createDataFrame(data, ["Name"])

# 1. Define Python function
def capitalize_str(val: str) -> str:
    if val is None:
        return None
    return val.upper()

# 2. Register UDF
capitalize_udf = udf(capitalize_str, StringType())

# 3. Apply UDF
df.withColumn("Name_Uppercase", capitalize_udf(df["Name"])).show()
