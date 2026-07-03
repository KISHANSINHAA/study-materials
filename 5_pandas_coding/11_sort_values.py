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

# Pandas program to sort values

import pandas as pd

data = {
    "name": ["Alice", "Bob", "Charlie"],
    "age": [35, 25, 30],
    "score": [90, 85, 95]
}
df = pd.DataFrame(data)

# Sort by age ascending, then score descending
sorted_df = df.sort_values(by=["age", "score"], ascending=[True, False])
print(sorted_df)
