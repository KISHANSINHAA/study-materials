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

# PySpark program to add or update columns

import os
import sys
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit

spark = SparkSession.builder.appName("AddNewColumn").master("local[*]").getOrCreate()

data = [("Alice", 5000), ("Bob", 6000)]
df = spark.createDataFrame(data, ["Name", "Salary"])

# Add new columns:
# 1. 'Bonus' as 10% of salary
# 2. 'Company' as static literal value using lit()
new_df = df.withColumn("Bonus", col("Salary") * 0.10) \
            .withColumn("Company", lit("Accenture"))

new_df.show()
