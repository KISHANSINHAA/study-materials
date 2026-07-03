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

# PySpark program showing Broadcast Join
# Optimization technique when joining a small DataFrame with a large DataFrame.
# Small DataFrame is sent to all executors to avoid data shuffling.

import os
import sys
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

from pyspark.sql import SparkSession
from pyspark.sql.functions import broadcast

spark = SparkSession.builder.appName("BroadcastJoin").master("local[*]").getOrCreate()

# Large DF
large_df = spark.createDataFrame([(1, "Product_X", 10), (2, "Product_Y", 20)], ["ID", "Product", "SupplierID"])
# Small DF to broadcast
small_df = spark.createDataFrame([(10, "Supplier_A"), (20, "Supplier_B")], ["SupplierID", "SupplierName"])

# Perform Broadcast Join
joined_df = large_df.join(broadcast(small_df), "SupplierID")
joined_df.show()
