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

# Pandas program to join DataFrames
# Joins DataFrames based on their Index.

import pandas as pd

df1 = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie"]
}, index=[1, 2, 3])

df2 = pd.DataFrame({
    "salary": [50000, 60000, 70000]
}, index=[2, 3, 4])

# Join df2 to df1 (left join by default)
joined = df1.join(df2, how="inner")
print("Joined DataFrames on Index:\n", joined)
