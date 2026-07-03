# ====================================================================
# THEORY & CONCEPT:
# Filtering rows and selecting columns are narrow transformations. They do not require data to be shuffled across nodes, as they operate independently on each partition in parallel.
#
# COMPLEXITY:
# Time Complexity: O(N) parallel scan.
# Space Complexity: O(1) auxiliary space (narrow dependency).
#
# INTERVIEW Q&A:
# Q: What is lazy evaluation in PySpark?
# A: Spark does not execute transformations (like filter or select) immediately. It builds a Directed Acyclic Graph (DAG) and executes it only when an action (like show, collect, or count) is called.
#
# Q: What is the difference between filter() and where() in PySpark?
# A: They are aliases of each other; they function identically.
# ====================================================================

# PySpark program to filter rows in a DataFrame
# Filters row based on values using .filter() or .where()

import os
import sys
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.appName("FilterData").master("local[*]").getOrCreate()

# Create Sample DataFrame
data = [("Alice", 25, "NY"), ("Bob", 30, "CA"), ("Charlie", 35, "NY"), ("David", 18, "TX")]
df = spark.createDataFrame(data, ["Name", "Age", "State"])

# Filter condition: Age > 25 AND State == "NY"
filtered_df = df.filter((col("Age") > 25) & (col("State") == "NY"))

print("Filtered DataFrame (Age > 25 & State == 'NY'):")
filtered_df.show()
