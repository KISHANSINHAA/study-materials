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

# Pandas unique() and nunique() functions

import pandas as pd

df = pd.DataFrame({
    "department": ["IT", "HR", "IT", "Sales", "HR", "IT"]
})

# Get unique values as an array
unique_depts = df["department"].unique()
# Get number of unique values
num_unique = df["department"].nunique()

print("Unique Departments:", unique_depts)
print("Count of Unique Departments:", num_unique)
