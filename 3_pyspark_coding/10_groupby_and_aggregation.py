# ====================================================================
# THEORY & CONCEPT:
# In distributed computing, grouping requires gathering matching keys onto the same executor partition. This causes a wide dependency (shuffle), which moves data across the network. Local aggregations are performed first to minimize network transfer.
#
# COMPLEXITY:
# Time Complexity: O(N log N) due to network transfer and sorting/grouping.
# Space Complexity: O(N) distributed memory.
#
# INTERVIEW Q&A:
# Q: What is a wide transformation in Spark?
# A: A transformation that requires data shuffling across the network (e.g. groupBy, join, repartition).
#
# Q: How does Spark optimize aggregates?
# A: Spark uses Map-Side Combiners to aggregate values locally on each partition before shuffling, reducing network payload.
# ====================================================================

# PySpark program for GroupBy and Aggregation
# Groups data by category and computes aggregate statistics (sum, average, count, max).

import os
import sys
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, avg, count, max

spark = SparkSession.builder.appName("GroupByAggregation").master("local[*]").getOrCreate()

data = [
    ("HR", "Alice", 5000),
    ("HR", "Bob", 6000),
    ("IT", "Charlie", 8000),
    ("IT", "David", 7500),
    ("Sales", "Emma", 4500)
]
df = spark.createDataFrame(data, ["Department", "Name", "Salary"])

# Group by Department and compute stats
agg_df = df.groupBy("Department").agg(
    count("Name").alias("EmployeeCount"),
    sum("Salary").alias("TotalSalary"),
    avg("Salary").alias("AverageSalary"),
    max("Salary").alias("MaxSalary")
)

print("Aggregated Salaries by Department:")
agg_df.show()
