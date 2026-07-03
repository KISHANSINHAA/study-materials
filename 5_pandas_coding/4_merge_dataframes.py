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

# Pandas program to merge DataFrames
# Similar to SQL Joins based on key columns.

import pandas as pd

df1 = pd.DataFrame({
    "emp_id": [1, 2, 3],
    "name": ["Alice", "Bob", "Charlie"]
})

df2 = pd.DataFrame({
    "emp_id": [2, 3, 4],
    "salary": [60000, 70000, 80000]
})

# Inner Merge
inner_merged = pd.merge(df1, df2, on="emp_id", how="inner")
print("Inner Merge:\n", inner_merged)

# Left Merge
left_merged = pd.merge(df1, df2, on="emp_id", how="left")
print("\nLeft Merge:\n", left_merged)
