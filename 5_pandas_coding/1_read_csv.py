# ====================================================================
# THEORY & CONCEPT:
# Pandas data wrangling. Manipulates structures in memory using vectorised operations on Series and DataFrames.
#
# COMPLEXITY:
# Time Complexity: O(N) vector operations.
# Space Complexity: O(N) RAM allocation.
#
# INTERVIEW Q&A:
# Q: What is vectorization in Pandas?
# A: Performing operations on entire arrays instead of looping through individual elements, leveraging fast underlying C libraries.
#
# Q: What is the difference between loc and iloc?
# A: loc accesses rows/columns by labels/names. iloc accesses them by integer index positions.
# ====================================================================

# Pandas program to read a CSV file
# Covers loading, schema information, and statistics.

import pandas as pd
import io

# Mock CSV text data
csv_data = '''name,age,salary,dept
Alice,25,50000,HR
Bob,30,60000,IT
Charlie,35,70000,IT
David,40,,Sales
'''

# Read CSV (using io.StringIO to simulate file reading)
df = pd.read_csv(io.StringIO(csv_data))

print("DataFrame Preview:\n", df)
print("\nDataFrame Info:")
print(df.info())
print("\nBasic Statistics:")
print(df.describe())
