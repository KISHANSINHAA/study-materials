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

# PySpark program to read a CSV file
# This shows initializing Spark Session and reading data with headers and schema inference.

# pyrefly: ignore [missing-import]
import os
import sys
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

from pyspark.sql import SparkSession


# Initialize Spark Session
spark = SparkSession.builder \
    .appName("ReadCSV") \
    .master("local[*]") \
    .getOrCreate()

# Read CSV with headers and inferSchema
# header=True treats the first line as column names
# inferSchema=True detects data types automatically
try:
    df = spark.read.csv("sample_data.csv", header=True, inferSchema=True)
    print("CSV schema:")
    df.printSchema()
    print("CSV data preview:")
    df.show(5)
except Exception as e:
    print("CSV file path does not exist. Created a mock DataFrame for display:")
    # Mock fallback
    mock_data = [("Alice", 25), ("Bob", 30)]
    df = spark.createDataFrame(mock_data, ["name", "age"])
    df.show()
